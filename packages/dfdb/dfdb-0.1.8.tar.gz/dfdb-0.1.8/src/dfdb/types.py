import warnings

from sqlalchemy.types import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Double,
    Integer,
    PickleType,
    SmallInteger,
    Text,
    Time,
)
from pandas._libs import lib
from pandas.util._exceptions import find_stack_level
import pandas as pd
import numpy as np

__all__ = ['infer_sqlalchemy_type', 'infer_pandas_type', 'result_sql_type']


def infer_sqlalchemy_type(col):
    """
    Code adapted from https://github.com/pandas-dev/pandas/blob/main/pandas/io/sql.py#1253 (as of 2023-04-11).
    Mostly the same, except that col can be a np.array or a scalar. Also, non-standard objects are inferred as
    sqlalchemy.PickleType instead of sqlalchemy.Text. (Under the hood, I believe PickleType is simply stored
    as a LargeBinary object, which in SQLite corresponds to BLOB)
    """
    col = pd.Series(col, copy=False)

    # Infer type of column, while ignoring missing values.
    # Needed for inserting typed data containing NULLs, GH 8778.
    col_type = lib.infer_dtype(col, skipna=True)

    if col_type in ("datetime64", "datetime"):
        # GH 9086: TIMESTAMP is the suggested type if the column contains
        # timezone information
        try:
            if col.dt.tz is not None:
                return TIMESTAMP(timezone=True)
        except AttributeError:
            # The column is actually a DatetimeIndex
            # GH 26761 or an Index with date-like data e.g. 9999-01-01
            if getattr(col, "tz", None) is not None:
                return TIMESTAMP(timezone=True)
        return DateTime
    if col_type == "timedelta64":
        warnings.warn(
            "the 'timedelta' type is not supported, and will be "
            "written as integer values (ns frequency) to the database.",
            UserWarning,
            stacklevel=find_stack_level(),
        )
        return BigInteger
    elif col_type == "floating":
        if col.dtype == "float32":
            return Float(precision=23)
        else:
            # return Float(precision=53)
            return Double()  # SQLite doesn't distinguish Float(23) and Float(53) (it is always Float(53)), so use Double() (new in SQLalchemy 2.0.0) to encode this information. As far as I can see, Double() represents Float(53) in all major SQL databases.
    elif col_type == "integer":
        # GH35076 Map pandas integer to optimal SQLAlchemy integer type
        if col.dtype.name.lower() in ("int8", "uint8", "int16"):
            return SmallInteger
        elif col.dtype.name.lower() in ("uint16", "int32"):
            return Integer
        elif col.dtype.name.lower() == "uint64":
            raise ValueError("Unsigned 64 bit integer datatype is not supported")
        else:
            return BigInteger
    elif col_type == "boolean":
        return Boolean
    elif col_type == "date":
        return Date
    elif col_type == "time":
        return Time
    elif col_type == "complex":
        raise ValueError("Complex datatypes not supported")
    elif col_type == "string":
        return Text
    elif col_type == "categorical":
        raise ValueError("Categorical datatypes not supported.")

    return PickleType


def infer_pandas_type(dtype, numpy_nullable=False, float_policy='lossless'):
    """
    Infer corresponding pandas data type from SQLalchemy data type.
    numpy_nullable has same meaning as in dtype_backend='numpy_nullable' in pd.read_sql
    float_policy indicates how to interpret the Float data type. If float_policy
    is 'allow_lossy', then interpret Float with no precision argument as float32.
    This allows for the preservation of data type when saving and then loading a dataframe
    using this package on SQLITE, since SQLite doesn't store precision info so I just call
    float32 FLOAT and float64 DOUBLE in SQLite. However, this could lead to loss of information,
    since FLOAT without precision argument is can mean float64.
    """
    available_policies = ['lossless', 'allow_lossy']
    if float_policy not in available_policies:
        raise ValueError(f"float_policy must be in {available_policies}.")

    dtype_name = type(dtype).__name__  # check name instead of using isinstance due to subclass issues

    if dtype_name == "TIMESTAMP":
        if dtype.timezone:
            raise NotImplementedError("conversion for type 'TIMESTAMP(timezone=True)' currently not supported.")
        return "datetime64[ns]"
    elif dtype_name in ["DateTime", "Date", "Time"]:
        return "datetime64[ns]"
    elif dtype_name == "Double":
        return "Float64" if numpy_nullable else "float64"
    elif dtype_name == "Float":
        if dtype.precision is not None:
            if dtype.precision > 24:
                return "Float64" if numpy_nullable else "float64"
            else:
                return "Float32" if numpy_nullable else "float32"
        else:
            if float_policy == 'allow_lossy':
                return "Float32" if numpy_nullable else "float32"
            else:
                return "Float64" if numpy_nullable else "float64"
    elif dtype_name == "SmallInteger":
        return "Int16" if numpy_nullable else "int16"
    elif dtype_name == "Integer":
        return "Int32" if numpy_nullable else "int32"
    elif dtype_name == "BigInteger":
        return "Int64" if numpy_nullable else "int64"
    elif dtype_name == "Boolean":
        return "boolean" if numpy_nullable else "bool"
    elif dtype_name == "Text":
        return "String" if numpy_nullable else "object"
    elif dtype_name == "Numeric":
        if dtype.asdecimal:
            return "object"
        return "Float64" if numpy_nullable else "float64"

    return "object"


def infer_np_type(dtype):
    dtype = infer_pandas_type(dtype)
    if dtype == 'boolean':
        return np.dtype('bool')
    elif dtype == 'String':
        return np.dtype('object')
    else:
        return np.dtype(dtype.lower())


def result_sql_type(*types, **kwargs):
    np_types = [infer_np_type(type) for type in types]
    np_type = np.result_type(*np_types)

    if np_type.kind == 'M':
        raise NotImplementedError("Currently can't distinguish between DateTime, Date, and Time")
    elif np_type.kind == 'm':
        warnings.warn(
            "the 'timedelta' type is not supported, and will be "
            "written as integer values (ns frequency) to the database.",
            UserWarning,
            stacklevel=find_stack_level(),
        )
        return BigInteger
    elif np_type.kind == 'f':
        if np_type.name == "float32":
            return Float(precision=23)
        else:
            # return Float(precision=53)
            return Double()  # SQLite doesn't distinguish Float(23) and Float(53) (it is always Float(53)), so use Double() (new in SQLalchemy 2.0.0) to encode this information. As far as I can see, Double() represents Float(53) in all major SQL databases.
    elif np_type.kind in 'iu':
        # GH35076 Map pandas integer to optimal SQLAlchemy integer type
        if np_type.name in ("int8", "uint8", "int16"):
            return SmallInteger()
        elif np_type.name in ("uint16", "int32"):
            return Integer()
        elif np_type.name == "uint64":
            raise ValueError("Unsigned 64 bit integer datatype is not supported")
        else:
            return BigInteger
    elif np_type.kind == 'b':
        return Boolean()
    elif np_type.kind == 'c':
        raise ValueError("Complex datatypes not supported")
    else:
        raise NotImplementedError("dtypes other than numeric and timedelta datatypes not currently implemented.")
