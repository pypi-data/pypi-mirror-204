import abc

import pandas as pd
import hyclib as lib

from . import (
    types,
    options,
)

@lib.clstools.attr_repr
class SQL(abc.ABC):
    def __init__(self, db, sql):
        self.db = db
        self.sql = sql

    def __str__(self):
        newline = '\n    '
        aligned = {k: str(v).replace('\n', newline + ' ' * (len(k) + 1)) for k, v in self.__dict__.items()}
        attrs = f",{newline}".join(f"{k}={v}" for k, v in aligned.items())
        return f'{type(self).__name__}({newline}{attrs}\n)'
    
    def fetch(self, **kwargs):
        kwargs = options.types | kwargs
        valid_keys = {'nullable_policy', 'float_policy'}
        if not set(kwargs).issubset(valid_keys):
            raise TypeError(f"keyword arguments of 'fetch' must be one of {valid_keys}.")
        
        nullable_policy = kwargs['nullable_policy']
        float_policy = kwargs['float_policy']
        
        valid_nullable_policies = {False, True, 'auto'}
        if nullable_policy not in valid_nullable_policies:
            raise TypeError(f"'nullable_policy' must be onf of {valid_nullable_policies}, but {nullable_policy=}.")
            
        numpy_nullable = False if nullable_policy in {False, 'auto'} else True
        
        with self.db.connect() as con:
            cur = con.execute(self.sql)
            rows = cur.fetchall()
            
        # use dtype='object' to prevent automatic type conversion which may modify elements
        df = pd.DataFrame(rows, columns=cur.keys(), copy=False, dtype='object')
        
        # manual type conversion
        for column_name, column in zip(df.columns, self.sql.subquery().columns):
            dtype = types.infer_pandas_type(column.type, numpy_nullable=numpy_nullable, float_policy=float_policy)
            if df[column_name].isna().any():
                if dtype.startswith('int'):
                    if nullable_policy == 'auto':
                        dtype = dtype.capitalize() # if it is integer and has NaN, then it must be a pandas Int ExtensionDtype
                    elif nullable_policy is False:
                        dtype = 'float64'
                elif dtype.startswith('bool'):
                    if nullable_policy == 'auto':
                        dtype = 'boolean' # if it is integer and has NaN, then it must be a pandas boolean ExtensionDtype
                    elif nullable_policy is False:
                        dtype = 'object'
            df[column_name] = df[column_name].astype(dtype)
            
        return df
    