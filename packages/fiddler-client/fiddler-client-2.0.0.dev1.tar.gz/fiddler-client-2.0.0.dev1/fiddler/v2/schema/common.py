import enum
import textwrap
from typing import Any, List, Optional, Union

import pandas as pd
from pydantic import Field

from fiddler.utils.formatting import prettyprint_number
from fiddler.v2.schema.base import BaseDataSchema


@enum.unique
class DataType(str, enum.Enum):
    """Supported datatypes for the Fiddler engine."""

    FLOAT = 'float'
    INTEGER = 'int'
    BOOLEAN = 'bool'
    STRING = 'str'
    CATEGORY = 'category'

    def is_numeric(self):
        return self.value in (DataType.INTEGER.value, DataType.FLOAT.value)

    def is_bool_or_cat(self):
        return self.value in (DataType.BOOLEAN.value, DataType.CATEGORY.value)

    def is_valid_target(self):
        return self.value != DataType.STRING.value


class Column(BaseDataSchema):
    """Represents a single column of a dataset or model input/output.

    :param name: The name of the column (corresponds to the header row of a
        CSV file)
    :param data_type: The best encoding type for this column's data.
    :param possible_values: If data_type is CATEGORY, then an exhaustive list
        of possible values for this category must be provided. Otherwise
        this field has no effect and is optional.
    :param is_nullable: Optional metadata. Tracks whether or not this column is
        expected to contain some null values.
    :param value_range_x: Optional metadata. If data_type is FLOAT or INTEGER,
        then these values specify a range this column's values are expected to
        stay within. Has no effect for non-numerical data_types.
    """

    name: str = Field(alias='column-name')
    data_type: DataType = Field(alias='data-type')
    possible_values: Optional[List[Any]] = Field(None, alias='possible-values')
    is_nullable: Optional[bool] = Field(None, alias='is-nullable')
    value_range_min: Optional[Union[int, float]] = Field(None, alias='value-range-min')
    value_range_max: Optional[Union[int, float]] = Field(None, alias='value-range-max')

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

    # # @TODO: Use pydantic validator
    # inappropriate_value_range = not self.data_type.is_numeric() and not (
    #     self.value_range_min is None and self.value_range_max is None
    # )
    # if inappropriate_value_range:
    #     raise ValueError(
    #         f'Do not pass `value_range` for '
    #         f'non-numerical {self.data_type} data type.'
    #     )

    @classmethod
    def from_dict(cls, desrialized_json: dict):
        return cls.parse_obj(desrialized_json)


class DatasetInfo(BaseDataSchema):
    columns: List[Column]

    def __repr__(self):
        column_info = textwrap.indent(repr(get_summary_dataframe(self.columns)), '    ')
        return f'DatasetInfo:\n' f'  columns:\n' f'{column_info}'

    def _repr_html_(self):
        column_info = self.get_summary_dataframe(self)
        return (
            f'<div style="border: thin solid rgb(41, 57, 141); padding: 10px;">'
            f'<h3 style="text-align: center; margin: auto;">DatasetInfo\n</h3>'
            f'<pre>display_name: {self.display_name}\nfiles: {self.files}\n</pre>'
            f'<hr>Columns:'
            f'{column_info._repr_html_()}'
            f'</div>'
        )


def get_summary_dataframe(columns: List[Column], placeholder='') -> pd.DataFrame:
    """
        Example:
                 column     dtype count(possible_values) is_nullable            value_range
    0       CreditScore   INTEGER                              False        376 - 850
    1         Geography  CATEGORY                      3       False
    2            Gender  CATEGORY                      2       False
    3               Age   INTEGER                              False         18 - 82
    4            Tenure   INTEGER                              False          0 - 10
    5           Balance     FLOAT                              False        0.0 - 213,100.0
    6     NumOfProducts   INTEGER                              False          1 - 4
    7         HasCrCard  CATEGORY                      2       False
    8    IsActiveMember  CATEGORY                      2       False
    9   EstimatedSalary     FLOAT                              False      371.1 - 199,700.0
    10          Churned  CATEGORY                      2       False

    """  # noqa E501
    column_names = []
    column_dtypes = []
    n_possible_values = []
    is_nullable = []
    mins: List[Any] = []
    maxes: List[Any] = []
    for column in columns:
        column_names.append(column.name)
        column_dtypes.append(column.data_type)
        n_possible_values.append(
            len(column.possible_values)
            if column.possible_values is not None
            else placeholder
        )
        is_nullable.append(
            str(column.is_nullable) if column.is_nullable is not None else placeholder
        )
        if not (column.data_type == 'int' or column.data_type == 'float'):
            mins.append(None)
            maxes.append(None)
        else:
            min_str = (
                prettyprint_number(column.value_range_min)
                if column.value_range_min is not None
                else '*'
            )
            max_str = (
                prettyprint_number(column.value_range_max)
                if column.value_range_max is not None
                else '*'
            )
            mins.append(min_str)
            maxes.append(max_str)
    range_pad_len = max(len(x) if x is not None else 0 for x in mins + maxes)
    value_range = [
        (placeholder if x is None else f'{x:>{range_pad_len}} - {y:<{range_pad_len}}')
        for x, y in zip(mins, maxes)
    ]
    return pd.DataFrame(
        {
            'column': column_names,
            'dtype': column_dtypes,
            'count(possible_values)': n_possible_values,
            'is_nullable': is_nullable,
            'value_range': value_range,
        }
    )
