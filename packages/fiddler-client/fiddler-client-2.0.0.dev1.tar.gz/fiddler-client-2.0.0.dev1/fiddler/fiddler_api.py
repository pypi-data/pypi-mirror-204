# TODO: Add License
import copy
import json
import tempfile
import textwrap
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import yaml
from deprecated import deprecated

from fiddler.api.publish_event import PublishEvent
from fiddler.connection import Connection
from fiddler.experimental import ExperimentalFeatures
from fiddler.project import Project
from fiddler.utils import logging
from fiddler.v2.constants import (
    CSV_EXTENSION,
    PARQUET_EXTENSION,
    SUPPORTABLE_FILE_EXTENSIONS,
)

from . import constants
from .core_objects import (
    BatchPublishType,
    DatasetInfo,
    DataType,
    DeploymentOptions,
    DeploymentType,
    FiddlerTimestamp,
    MLFlowParams,
    ModelInfo,
    ModelTask,
    MonitoringViolation,
    MonitoringViolationType,
    SegmentInfo,
)
from .monitoring_validator import MonitoringValidator
from .utils import cast_input_data
from .utils.general_checks import do_not_proceed, safe_name_check, type_enforce
from .utils.pandas import df_size_exceeds, write_dataframe_to_parquet_file

LOG = logging.getLogger(__name__)

SUCCESS_STATUS = Connection.SUCCESS_STATUS
FAILURE_STATUS = Connection.FAILURE_STATUS
FIDDLER_ARGS_KEY = Connection.FIDDLER_ARGS_KEY
STREAMING_HEADER_KEY = Connection.STREAMING_HEADER_KEY
AUTH_HEADER_KEY = Connection.AUTH_HEADER_KEY
ROUTING_HEADER_KEY = Connection.ROUTING_HEADER_KEY
ADMIN_SERVICE_PORT = 4100
DATASET_MAX_ROWS = 50_000

# A PredictionEventBundle represents a batch of inferences and their input
# features. All of these share schema, latency, and success status. A bundle
# can consist just one event as well.
PredictionEventBundle = namedtuple(
    'PredictionEventBundle',
    [
        'prediction_status',  # typeof: int # 0 for success, failure otherwise
        'prediction_latency',  # typeof: float # Latency in seconds.
        'input_feature_bundle',  # list of feature vectors.
        'prediction_bundle',  # list of prediction vectors.
        # TODO: Support sending schema as well.
    ],
)

_protocol_version = 1


class FiddlerApi:
    """Broker of all connections to the Fiddler API.
    Conventions:
        - Exceptions are raised for FAILURE reponses from the backend.
        - Methods beginning with `list` fetch lists of ids (e.g. all model ids
            for a project) and do not alter any data or state on the backend.
        - Methods beginning with `get` return a more complex object but also
            do not alter data or state on the backend.
        - Methods beginning with `run` invoke model-related execution and
            return the result of that computation. These do not alter state,
            but they can put a heavy load on the computational resources of
            the Fiddler engine, so they should be paralellized with care.
        - Methods beginning with `delete` permanently, irrevocably, and
            globally destroy objects in the backend. Think "rm -rf"
        - Methods beginning with `upload` convert and transmit supported local
            objects to Fiddler-friendly formats loaded into the Fiddler engine.
            Attempting to upload an object with an identifier that is already
            in use will result in an exception being raised, rather than the
            existing object being overwritten. To update an object in the
            Fiddler engine, please call both the `delete` and `upload` methods
            pertaining to the object in question.

    :param url: The base URL of the API to connect to. Usually either
        https://dev.fiddler.ai (cloud) or http://localhost:4100 (onebox)
    :param org_id: The name of your organization in the Fiddler platform
    :param auth_token: Token used to authenticate. Your token can be
        created, found, and changed at <FIDDLER URL>/settings/credentials.
    :param proxies: optionally, a dict of proxy URLs. e.g.,
                    proxies = {'http' : 'http://proxy.example.com:1234',
                               'https': 'https://proxy.example.com:5678'}
    :param verbose: if True, api calls will be logged verbosely,
                    *warning: all information required for debugging will be
                    logged including the auth_token.
    :param verify: if False, certificate verification will be disabled when
        establishing an SSL connection.
    """

    def __init__(
        self,
        url=None,
        org_id=None,
        auth_token=None,
        proxies=None,
        verbose=False,
        timeout: int = None,
        verify=True,
    ):
        self.org_id = org_id
        self.strict_mode = True
        self.connection = Connection(
            url, org_id, auth_token, proxies, verbose, timeout, verify=verify
        )

        self.monitoring_validator = MonitoringValidator()
        self.experimental = ExperimentalFeatures(client=self)

    def __getattr__(self, function_name):
        """
        Overriding allows us to point unrecognized use cases to the documentation page
        """

        def method(*args, **kwargs):
            # This is a method that is not recognized
            error_msg = (
                f'Function `{function_name}` not found.\n'
                f'Please consult Fiddler documentation at `https://api.fiddler.ai/`'
            )
            raise RuntimeError(error_msg)

        return method

    @staticmethod
    def _abort_dataset_upload(
        dataset: Dict[str, pd.DataFrame], size_check_enabled: bool, max_len: int
    ):
        """
        This method checks if any of the dataframes exeeds size limit.
        In case the size limit is exceeded and size_check_enabled is True
        a warning is issued and the user is required to confirm if they'd
        like to proceed with the upload
        """
        # check if the dataset exceeds size limits
        warn_and_query = size_check_enabled and df_size_exceeds(dataset, max_len)
        if warn_and_query:
            LOG.warning(
                f'The dataset contains more than {max_len} datapoints. '
                f'Please allow for additional time to upload the dataset '
                f'and calculate statistical metrics. '
                f'To disable this message set the flag size_check_enabled to False. '
                f'\n\nAlternately, consider sampling the dataset. '
                f'If you plan to sample the dataset please ensure that the '
                f'representative sample captures all possible '
                f'categorical features, labels and numerical ranges that '
                f'would be encountered during deployment.'
                f'\n\nFor details on how datasets are used and considerations '
                f'for when large datasets are necessary, please refer to '
                f'https://docs.fiddler.ai/pages/user-guide/administration-concepts/project-structure/#dataset'
            )
            user_query = 'Would you like to proceed with the upload (y/n)? '
            return do_not_proceed(user_query)
        return False

    def _check_connection(self, check_client_version=True, check_server_version=True):
        return self.connection.check_connection(
            check_client_version, check_server_version
        )

    def _call_executor_service(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
    ):
        return self.connection.call_executor_service(
            path, json_payload, files, is_get_request, stream
        )

    def _call(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
        timeout: Optional[int] = None,
        num_tries: int = 1,
    ):
        """Issues a request to the API and returns the result,
        logigng and handling errors appropriately.

        Raises a RuntimeError if the response is a failure or cannot be parsed.
        Does not handle any ConnectionError exceptions thrown by the `requests`
        library.

        Note: Parameters `timeout` and `num_tries` are currently only utilized in a workaround
        for a bug involving Mac+Docker communication. See: https://github.com/docker/for-mac/issues/3448
        """
        return self.connection.call(
            path, json_payload, files, is_get_request, stream, timeout, num_tries
        )

    @deprecated(
        reason='Please use get_datasets, this method will be removed in future versions'
    )
    def list_datasets(self, project_id: str) -> List[str]:
        """List the ids of all datasets in the organization.

        :returns: List of strings containing the ids of each dataset.
        """
        return self.project(project_id).list_datasets()

    @deprecated(
        reason='Please use get_projects, this method will be removed in future versions'
    )
    def list_projects(self, get_project_details: bool = False) -> List[str]:
        """List the ids of all projects in the organization.

        :returns: List of strings containing the ids of each project.
        """
        path = ['list_projects', self.org_id]

        payload = {
            'project_details': get_project_details,
        }

        return self._call(path, json_payload=payload)['projects']

    def project(self, project_id):
        return Project(self.connection, project_id)

    @deprecated(
        reason='Please use get_models, this method will be removed in future versions'
    )
    def list_models(self, project_id: str) -> List[str]:
        """List the names of all models in a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :returns: List of strings containing the ids of each model in the
            specified project.
        """
        return self.project(project_id).list_models()

    @deprecated(
        reason='Please use get_dataset, this method will be removed in future versions'
    )
    def get_dataset_info(self, project_id: str, dataset_id: str) -> DatasetInfo:
        """Get DatasetInfo for a dataset.

        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: A fiddler.DatasetInfo object describing the dataset.
        """
        return self.project(project_id).dataset(dataset_id).get_info()

    @deprecated(
        reason='Please use get_model, this method will be removed in future versions'
    )
    def get_model_info(self, project_id: str, model_id: str) -> ModelInfo:
        """Get ModelInfo for a model in a certain project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: A fiddler.ModelInfo object describing the model.
        """
        return self.project(project_id).model(model_id).get_info()

    def _query_dataset(
        self,
        project_id: str,
        dataset_id: str,
        fields: List[str],
        max_rows: int,
        split: Optional[str] = None,
        sampling=False,
        sampling_seed=0.0,
    ):
        return (
            self.project(project_id)
            .dataset(dataset_id)
            ._query_dataset(fields, max_rows, split, sampling, sampling_seed)
        )

    @deprecated(
        reason='Please use get_slice, this method will be removed in future versions'
    )
    def get_dataset(
        self,
        project_id: str,
        dataset_id: str,
        max_rows: int = 1_000,
        splits: Optional[List[str]] = None,
        sampling=False,
        dataset_info: Optional[DatasetInfo] = None,
        include_fiddler_id=False,
    ) -> Dict[str, pd.DataFrame]:
        """Fetches data from a dataset on Fiddler.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.
        :param max_rows: Up to this many rows will be fetched from eash split
            of the dataset.
        :param splits: If specified, data will only be fetched for these
            splits. Otherwise, all splits will be fetched.
        :param sampling: If True, data will be sampled up to max_rows. If
            False, rows will be returned in order up to max_rows. The seed
            will be fixed for sampling.∂
        :param dataset_info: If provided, the API will skip looking up the
            DatasetInfo (a necessary precursor to requesting data).
        :param include_fiddler_id: Return the Fiddler engine internal id
            for each row. Useful only for debugging.

        :returns: A dictionary of str -> DataFrame that maps the name of
            dataset splits to the data in those splits. If len(splits) == 1,
            returns just that split as a dataframe, rather than a dataframe.
        """
        return (
            self.project(project_id)
            .dataset(dataset_id)
            .download(max_rows, splits, sampling, dataset_info, include_fiddler_id)
        )

    def delete_dataset(self, project_id: str, dataset_id: str):
        """Permanently delete a dataset.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).dataset(dataset_id).delete()

    def delete_model(
        self, project_id: str, model_id: str, delete_prod=True, delete_pred=True
    ):
        """Permanently delete a model.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param delete_prod: Boolean value to delete the production table.
            By default this table is dropped.
        :param delete_pred: Boolean value to delete the prediction table.
            By default this table is dropped.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).model(model_id).delete(delete_prod, delete_pred)

    def _delete_model_artifacts(self, project_id: str, model_id: str):
        """Permanently delete a model artifacts.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).model(model_id)._delete_artifacts()

    def delete_project(self, project_id: str):
        """Permanently delete a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        # Type enforcement
        return self.project(project_id).delete()

    ##### Start: Methods related to uploading dataset #####

    def _upload_dataset_files(
        self,
        project_id: str,
        dataset_id: str,
        file_paths: List[Path],
        dataset_info: Optional[DatasetInfo] = None,
    ):
        """Uploads data files to the Fiddler platform."""
        safe_name_check(dataset_id, constants.MAX_ID_LEN, self.strict_mode)

        payload: Dict[str, Any] = dict(dataset_name=dataset_id)

        if dataset_info is not None:
            if self.strict_mode:
                dataset_info.validate()

            payload['dataset_info'] = dict(dataset=dataset_info.to_dict())

        payload['split_test'] = False
        path = ['dataset_upload', self.org_id, project_id]

        LOG.info(f'Uploading the dataset {dataset_id} ...')

        result = self._call(path, json_payload=payload, files=file_paths)

        return result

    def upload_dataset(
        self,
        project_id: str,
        dataset: Dict[str, pd.DataFrame],
        dataset_id: str,
        info: Optional[DatasetInfo] = None,
        size_check_enabled: bool = True,
    ):
        """Uploads a representative dataset to the Fiddler engine.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param dataset: A dictionary mapping name -> DataFrame
            containing data to be uploaded to the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine. Must be a short string without whitespace.
        :param info: A DatasetInfo object specifying all the details of the
            dataset. If not provided, a DatasetInfo will be inferred from the
            dataset and a warning raised.
        :param size_check_enabled: Flag to enable the dataframe size check.
            Default behavior is to raise a warning and present an interactive
            dialogue if the size of the dataframes exceeds the default limit.
            Set this flag to False to disable the checks.

        :returns: The server response for the upload.
        """
        # Type enforcement
        # @question: Shouldn't we just throw this as an error from server if we already don't do it?
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        assert (
            ' ' not in dataset_id
        ), 'The dataset identifier should not contain whitespace'
        safe_name_check(dataset_id, constants.MAX_ID_LEN, self.strict_mode)

        # get a dictionary of str -> pd.DataFrame for all data to upload
        if not isinstance(dataset, dict):
            raise ValueError('dataset must be a dictionary mapping name -> DataFrame')

        # check if the dataset exceeds size limits
        # @todo: why is checking for filesize even an option, shouldn't it be default?
        abort_upload = self._abort_dataset_upload(
            dataset, size_check_enabled, DATASET_MAX_ROWS
        )
        if abort_upload:
            raise RuntimeError('Dataset upload aborted.')

        if info:
            # Since we started populating stats recently, some older yamls
            # dont have it. Or the user might just supply us the basic
            # schema without stats.
            # If the user provided the schema/yaml file, ask the user to
            # re-create dataset info with:
            # info = DatasetInfo.update_stats_for_existing_schema(dataset,
            # info, max_inferred_cardinality)
            # @question: shouldn't these validations be part of DatasetInfo? (high cohesion) and we invoke the method here.
            for column in info.columns:
                if (
                    (column.value_range_min is None) or (column.value_range_max is None)
                ) and column.data_type.is_numeric():
                    raise ValueError(
                        f'Dataset info does not contain min/max values for the numeric feature {column.name}. '
                        f'Please update using fdl.DatasetInfo.update_stats_for_existing_schema() '
                        f'and upload dataset with the updated dataset info.'
                    )
                if (not column.possible_values) and (
                    column.data_type.value
                    in [DataType.CATEGORY.value, DataType.BOOLEAN.value]
                ):
                    raise ValueError(
                        f'Dataset info does not contain possible values for the categorical feature {column.name}. '
                        f'Please update using fdl.DatasetInfo.update_stats_for_existing_schema() '
                        f'and upload dataset with the updated dataset info.'
                    )

            # Validate column names
            for name, df in dataset.items():
                for info_column in info.columns:
                    if info_column.name not in df:
                        raise RuntimeError(
                            f'{info_column.name}({name}) column not found in the dataframe, '
                            f'but passed in the info'
                        )

        # use inferred info with a warning if not `info` is passed
        else:
            inferred_info = DatasetInfo.from_dataframe(
                df=dataset.values(),
                display_name=dataset_id,
                dataset_id=dataset_id,
                max_inferred_cardinality=1000,
            )
            # @question: we only do validation when info is passed and not when it is inferred? Why should this be the case?
            LOG.warning(
                f'Heads up! We are inferring the details of your dataset from '
                f'the dataframe(s) provided. Please take a second to check '
                f'our work.'
                f'\n\nIf the following DatasetInfo is an incorrect '
                f'representation of your data, you can construct a '
                f'DatasetInfo with the DatasetInfo.from_dataframe() method '
                f'and modify that object to reflect the correct details of '
                f'your dataset.'
                f'\n\nAfter constructing a corrected DatasetInfo, please '
                f're-upload your dataset with that DatasetInfo object '
                f'explicitly passed via the `info` parameter of '
                f'FiddlerApi.upload_dataset().'
                f'\n\nYou may need to delete the initially uploaded version'
                f"via FiddlerApi.delete_dataset('{dataset_id}')."
                f'\n\nInferred DatasetInfo to check:'
                f'\n{textwrap.indent(repr(inferred_info), "  ")}'
            )
            info = inferred_info

        if self.strict_mode:
            info.validate()

        return self._upload_dataset_with_compression(
            project_id=project_id,
            dataset=dataset,
            dataset_id=dataset_id,
            dataset_info=info,
        )

    def upload_dataset_from_dir(
        self,
        project_id: str,
        dataset_id: str,
        dataset_dir: Path,
        file_type: str = 'csv',
        file_schema=None,
        size_check_enabled: bool = False,
    ):
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)
        dataset_dir = type_enforce('dataset_dir', dataset_dir, Path)

        if f'.{file_type}' not in SUPPORTABLE_FILE_EXTENSIONS:
            raise ValueError(
                f'Invalid file_type :{file_type}. Valid file types are : '
                f'{SUPPORTABLE_FILE_EXTENSIONS}'
            )

        if not dataset_dir.is_dir():
            raise ValueError(f'{dataset_dir} is not a directory')

        dataset_yaml = dataset_dir / f'{dataset_id}.yaml'

        if not dataset_yaml.is_file():
            raise ValueError(f'YAML file not found: {dataset_yaml}')

        with dataset_yaml.open() as f:
            dataset_info = DatasetInfo.from_dict(yaml.safe_load(f))

        files = dataset_dir.glob('*.csv')
        csv_files = [x for x in files if x.is_file()]

        LOG.info(f'Found CSV file {csv_files}')

        # Lets make sure that we add stats if they are not already there.
        # We need to read the datasets in pandas and create a dataset dictionary
        dataset = {}
        csv_paths = []
        for file in csv_files:
            csv_name = str(file).split('/')[-1]
            csv_paths.append(csv_name)
            name = csv_name[:-4]

            # @TODO Change the flow so that we can read the CSV in chunks
            dataset[name] = pd.read_csv(file, dtype=dataset_info.get_pandas_dtypes())

        # check if the dataset exceeds size limits
        abort_upload = self._abort_dataset_upload(
            dataset, size_check_enabled, DATASET_MAX_ROWS
        )
        if abort_upload:
            raise RuntimeError('Dataset upload aborted.')

        # Update stats
        dataset_info = DatasetInfo.update_stats_for_existing_schema(
            dataset, dataset_info
        )
        updated_infos = []
        for item in dataset.values():
            update_info = DatasetInfo.check_and_update_column_info(dataset_info, item)
            updated_infos.append(update_info)

        dataset_info = DatasetInfo.as_combination(
            updated_infos, display_name=dataset_info.display_name
        )

        return self._upload_dataset_with_compression(
            project_id=project_id,
            dataset=dataset,
            dataset_id=dataset_id,
            dataset_info=dataset_info,
        )

    def _upload_dataset_with_compression(
        self,
        project_id: str,
        dataset: Dict[str, pd.DataFrame],
        dataset_id: str,
        dataset_info: DatasetInfo,
    ):
        schema = dataset_info.get_arrow_schema()

        # dump the data to named parquet temp file
        with tempfile.TemporaryDirectory() as tmp:
            file_paths = []
            for name, df in dataset.items():
                # Adding .csv to support legacy way of converting everything to CSV
                filename = f'{name}.{CSV_EXTENSION}.{PARQUET_EXTENSION}'
                file_path = Path(tmp) / filename
                file_paths.append(file_path)

                # Data type conversion as per dataset_info
                # Data types like date/time/datetime should be converted to string before creating parquet file
                df = df.astype(dtype=dataset_info.get_pandas_dtypes())

                write_dataframe_to_parquet_file(
                    df=df, file_path=file_path, schema=schema
                )

            # add files to the DatasetInfo on the fly
            dataset_info = copy.deepcopy(dataset_info)
            dataset_info.files = [
                fp.name.replace(f'.{PARQUET_EXTENSION}', '') for fp in file_paths
            ]

            # upload the parquet files
            LOG.info(f'[{dataset_id}] dataset upload: upload and import dataset files')

            res = self._upload_dataset_files(
                project_id=project_id,
                dataset_id=dataset_id,
                file_paths=file_paths,
                dataset_info=dataset_info,
            )

            LOG.info(f'Dataset uploaded {res}')
            return res

    ##### End: Methods related to uploading dataset #####

    def get_mutual_information(
        self,
        project_id: str,
        dataset_id: str,
        features: list,
        normalized: Optional[bool] = False,
        slice_query: Optional[str] = None,
        sample_size: Optional[int] = None,
        seed: Optional[float] = 0.25,
    ):
        """
        The Mutual information measures the dependency between two random variables.
        It's a non-negative value. If two random variables are independent MI is equal to zero.
        Higher MI values means higher dependency.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param features: list of features to compute mutual information with respect to all the variables in the dataset.
        :param normalized: If set to True, it will compute Normalized Mutual Information (NMI)
        :param slice_query: Optional slice query
        :param sample_size: Optional sample size for the selected dataset
        :param seed: Optional seed for sampling
        :return: a dictionary of mutual information w.r.t the given features.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        if isinstance(features, str):
            features = [features]
        if not isinstance(features, list):
            raise ValueError(
                f'Invalid type: {type(features)}. Argument features has to be a list'
            )
        correlation = {}
        for col_name in features:
            payload = dict(
                col_name=col_name,
                normalized=normalized,
                slice_query=slice_query,
                sample_size=sample_size,
                seed=seed,
            )
            path = ['dataset_mutual_information', self.org_id, project_id, dataset_id]
            res = self._call(path, json_payload=payload)
            correlation[col_name] = res
        return correlation

    @deprecated(
        reason='Please use add_project, this method will be removed in future versions'
    )
    def create_project(self, project_id: str):
        """Create a new project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine. Must be a short string without whitespace.

        :returns: Server response for creation action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)

        safe_name_check(project_id, constants.MAX_ID_LEN, self.strict_mode)
        res = None
        try:
            path = ['new_project', self.org_id, project_id]
            res = self._call(path)
        except Exception as e:
            if 'already exists' in str(e):
                LOG.error(
                    'Project name already exists, please try with a different name (You may not have access to all the projects)'
                )
            else:
                raise e

        return res

    ##### Start: Methods related to publishing event #####

    def _basic_drift_checks(self, project_id, model_info, model_id):
        # Lets make sure prediction table is created and has prediction data by
        # just running the slice query
        violations = []
        try:
            query_str = f'select * from "{model_info.datasets[0]}.{model_id}" limit 1'
            df = self.get_slice(
                query_str,
                project_id=project_id,
            )
            for index, row in df.iterrows():
                for out_col in model_info.outputs:
                    if out_col.name not in row:
                        msg = f'Drift error: {out_col.name} not in predictions table. Please delete and re-register your model.'
                        violations.append(
                            MonitoringViolation(MonitoringViolationType.WARNING, msg)
                        )
        except RuntimeError:
            msg = 'Drift error: Predictions table does not exists. Please run trigger_pre_computation for an existing model, or use register_model to register a new model.'
            violations.append(MonitoringViolation(MonitoringViolationType.WARNING, msg))
            return violations

        return violations

    def publish_event(
        self,
        project_id: str,
        model_id: str,
        event: dict,
        event_id: Optional[str] = None,
        update_event: Optional[bool] = None,
        event_timestamp: Optional[int] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        casting_type: Optional[bool] = False,
        dry_run: Optional[bool] = False,
    ):
        """
        Publishes an event to Fiddler Service.
        :param project_id: The project to which the model whose events are being published belongs
        :param model_id: The model whose events are being published
        :param dict event: Dictionary of event details, such as features and predictions.
        :param event_id: Unique str event id for the event
        :param update_event: Bool indicating if the event is an update to a previously published row
        :param event_timestamp: The UTC timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param timestamp_format:   Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
        the type referenced in model info. Default to False.
        :param dry_run: If true, the event isnt published and instead the user gets a report which shows
        IF the event along with the model would face any problems with respect to monitoring

        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        event = type_enforce('event', event, dict)
        if event_id:
            event_id = type_enforce('event_id', event_id, str)

        if casting_type:
            try:
                model_info = self.get_model_info(project_id, model_id)
            except RuntimeError:
                raise RuntimeError(
                    f'Did not find ModelInfo for project "{project_id}" and model "{model_id}".'
                )
            event = cast_input_data(event, model_info)

        if not timestamp_format or timestamp_format not in FiddlerTimestamp:
            raise ValueError('Please specify a valid timestamp_format')

        assert timestamp_format is not None, 'timestamp_format unexpectedly None'
        event['__timestamp_format'] = timestamp_format.value

        if update_event:
            event['__event_type'] = 'update_event'
            event['__updated_at'] = event_timestamp
            if event_id is None:
                raise ValueError('An update event needs an event_id')
        else:
            event['__event_type'] = 'execution_event'
            event['__occurred_at'] = event_timestamp

        if event_id is not None:
            event['__event_id'] = event_id

        if dry_run:
            violations = self._pre_flight_monitoring_check(project_id, model_id, event)
            violations_list = []
            LOG.info('\n****** publish_event dry_run report *****')
            LOG.info(f'Found {len(violations)} Violations:')
            for violation in violations:
                violations_list.append(
                    {'type': violation.type.value, 'desc': violation.desc}
                )
                LOG.info(f'Type: {violation.type.value: <11}{violation.desc}')
            result = json.dumps(violations_list)
        else:
            path = ['external_event', self.org_id, project_id, model_id]
            # The ._call uses `timeout` and `num_tries` logic due to an issue with Mac/Docker.
            # This is only enabled using the env variable `FIDDLER_RETRY_PUBLISH`; otherwise it
            # is a normal ._call function
            result = self._call(path, event, timeout=2, num_tries=5)

        return result

    def _pre_flight_monitoring_check(self, project_id, model_id, event):
        violations = []
        violations += self._basic_monitoring_tests(project_id, model_id)
        if len(violations) == 0:
            model_info = self.get_model_info(project_id, model_id)
            dataset_info = self.get_dataset_info(project_id, model_info.datasets[0])
            violations += self._basic_drift_checks(project_id, model_info, model_id)
            violations += self.monitoring_validator.pre_flight_monitoring_check(
                event, model_info, dataset_info
            )
        return violations

    def _basic_monitoring_tests(self, project_id, model_id):
        """Basic checks which would prevent monitoring from working altogether."""
        violations = []
        try:
            model_info = self.get_model_info(project_id, model_id)
        except RuntimeError:
            msg = f'Error: Model:{model_id} in project:{project_id} does not exist'
            violations.append(MonitoringViolation(MonitoringViolationType.FATAL, msg))
            return violations

        try:
            _ = self.get_dataset_info(project_id, model_info.datasets[0])
        except RuntimeError:
            msg = f'Error: Dataset:{model_info.datasets[0]} does not exist'
            violations.append(MonitoringViolation(MonitoringViolationType.FATAL, msg))
            return violations

        return violations

    def publish_events_batch(  # noqa
        self,
        project_id: str,
        model_id: str,
        batch_source: Union[pd.DataFrame, str],
        id_field: Optional[str] = None,
        update_event: Optional[bool] = False,
        timestamp_field: Optional[str] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        data_source: Optional[BatchPublishType] = None,
        casting_type: Optional[bool] = False,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
    ):
        """
        Publishes a batch events object to Fiddler Service.
        :param project_id:    The project to which the model whose events are being published belongs.
        :param model_id:      The model whose events are being published.
        :param batch_source:  Batch object to be published. Can be one of: Pandas DataFrame, CSV file, PKL Pandas DataFrame, or Parquet file.
        :param id_field:  Column to extract id value from.
        :param update_event: Bool indicating if the events are updates to previously published rows
        :param timestamp_field:     Column to extract timestamp value from.
                              Timestamp must match the specified format in `timestamp_format`.
        :param timestamp_format:   Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param data_source:   Source of batch object. In case of failed inference, can be one of:
                                - BatchPublishType.DATAFRAME
                                - BatchPublishType.LOCAL_DISK
                                - BatchPublishType.AWS_S3
                                - BatchPublishType.GCP_STORAGE
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
                             the type referenced in model info. Default to False.
        :param credentials:  Dictionary containing authorization for AWS or GCP.

                             For AWS S3, list of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.

                             For GCP, list of expected keys are
                              ['gcs_access_key_id', 'gcs_secret_access_key', 'gcs_session_token']
                              with 'gcs_session_token' being applicable to the GCP account being used.
        :param group_by: Column to group events together for Model Performance metrics. For example,
                         in ranking models that column should be query_id or session_id, used to
                         compute NDCG and MAP. Be aware that the batch_source file/dataset provided should have
                         events belonging to the SAME query_id/session_id TOGETHER and cannot be mixed
                         in the file. For example, having a file with rows belonging to query_id 31,31,31,2,2,31,31,31
                         would not work. Please sort the file by group_by group first to have rows with
                         the following order: query_id 31,31,31,31,31,31,2,2.
        """
        return PublishEvent(self.connection).publish_events_batch(
            project_id,
            model_id,
            batch_source,
            id_field,
            update_event,
            timestamp_field,
            timestamp_format,
            data_source,
            casting_type,
            credentials,
            group_by,
        )

    def publish_events_batch_schema(  # noqa
        self,
        batch_source: Union[pd.DataFrame, str],
        publish_schema: Dict[str, Any],
        data_source: Optional[BatchPublishType] = None,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
    ):
        """
        Publishes a batch events object to Fiddler Service.
        :param batch_source:  Batch object to be published. Can be one of: Pandas DataFrame, CSV file, PKL Pandas DataFrame, or Parquet file.
        :param publish_schema: Dict object specifying layout of data.
        :param data_source:   Source of batch object. In case of failed inference, can be one of:
                                - BatchPublishType.DATAFRAME
                                - BatchPublishType.LOCAL_DISK
                                - BatchPublishType.AWS_S3
                                - BatchPublishType.GCP_STORAGE
        :param credentials:  Dictionary containing authorization for AWS or GCP.

                             For AWS S3, list of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.

                             For GCP, list of expected keys are
                              ['gcs_access_key_id', 'gcs_secret_access_key', 'gcs_session_token']
                              with 'gcs_session_token' being applicable to the GCP account being used.
        :param group_by: Column to group events together for Model Performance metrics. For example,
                         in ranking models that column should be query_id or session_id, used to
                         compute NDCG and MAP.
        """
        return PublishEvent(self.connection).publish_events_batch_schema(
            batch_source,
            publish_schema,
            data_source,
            credentials,
            group_by,
        )

    ##### End: Methods related to publishing event #####

    def get_model(self, project_id: str, model_id: str, output_dir: Path):
        """
        download the model binary, package.py and model.yaml to the given
        output dir.

        :param project_id: project id
        :param model_id: model id
        :param output_dir: output directory
        :return: model artifacts
        """
        return self.project(project_id).model(model_id).download(output_dir)
