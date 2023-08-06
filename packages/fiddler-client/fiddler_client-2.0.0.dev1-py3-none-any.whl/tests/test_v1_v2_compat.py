import unittest

import pandas as pd

from fiddler.core_objects import BatchPublishType
from fiddler.v1_v2_compat import V1V2Compat
from tests.v2.base import BaseTestCase


class TestEventsAPI(BaseTestCase):
    def setUp(self) -> None:
        super(TestEventsAPI, self).setUp()
        self.v1v2Compat = V1V2Compat(client_v2=self.client)
        self.project_id = 'test_project'
        self.model_id = 'test_model'

    def test_publish_event_batch_client_v1_data_source_not_implemented(self):
        invalid_types_for_v1 = [BatchPublishType.AWS_S3, BatchPublishType.GCP_STORAGE]
        for invalid_source_type in invalid_types_for_v1:
            with self.assertRaises(NotImplementedError) as cx:
                self.v1v2Compat.publish_events_batch(
                    project_id=self.project_id,
                    model_id=self.model_id,
                    batch_source='path-string',
                    timestamp_field='timestamp',
                    data_source=invalid_source_type,
                )
            self.assertEqual(
                str(cx.exception),
                f'support for data_source type of {invalid_source_type} is not yet implemented',
            )

    def test_publish_event_batch_client_v1_data_source_mismatch(self):
        with self.assertRaises(ValueError) as cx:
            self.v1v2Compat.publish_events_batch(
                project_id=self.project_id,
                model_id=self.model_id,
                batch_source='path-string',
                data_source=BatchPublishType.DATAFRAME,
                timestamp_field='timestamp',
            )
        self.assertEqual(
            str(cx.exception),
            'based on the provided data_source type (BatchPublishType.DATAFRAME), '
            "expecting batch_source to be a pandas DataFrame, but instead found a <class 'str'>",
        )

        with self.assertRaises(ValueError) as cx:
            self.v1v2Compat.publish_events_batch(
                project_id=self.project_id,
                model_id=self.model_id,
                batch_source=pd.DataFrame(),
                data_source=BatchPublishType.LOCAL_DISK,
                timestamp_field='timestamp',
            )
        self.assertEqual(
            str(cx.exception),
            'based on the provided data_source type (BatchPublishType.LOCAL_DISK), '
            "expecting batch_source to be a filepath string, but instead found a <class 'pandas.core.frame.DataFrame'>",
        )

    def test_publish_event_batch_client_v1_invalid_batch_source_type(self):
        invalid_batch_sources_for_v1 = [None, pd.Series()]
        for invalid_batch_source in invalid_batch_sources_for_v1:
            with self.assertRaises(ValueError) as cx:
                self.v1v2Compat.publish_events_batch(
                    project_id=self.project_id,
                    model_id=self.model_id,
                    batch_source=invalid_batch_source,
                    timestamp_field='timestamp',
                )
            self.assertEqual(
                str(cx.exception),
                'batch_source must be either a filepath string or a pandas DataFrame',
            )

    def test_publish_events_dataframe_empty(self):
        with self.assertRaises(ValueError) as context:
            self.v1v2Compat.publish_events_batch(
                project_id=self.project_id,
                model_id=self.model_id,
                batch_source=pd.DataFrame(),
                timestamp_field='timestamp',
            )
        self.assertEqual(
            str(context.exception),
            'The batch provided is empty. Please retry with at least one row of data.',
        )


if __name__ == '__main__':
    unittest.main()
