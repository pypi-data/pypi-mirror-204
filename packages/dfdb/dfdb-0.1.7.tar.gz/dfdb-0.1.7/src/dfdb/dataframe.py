import collections
import itertools
import functools
import sys
import copy
import html
import numbers

import pandas as pd
import numpy as np
import sqlalchemy as sa
import hyclib as lib

from . import (
    abc,
    parsing,
    types,
    alter,
    options,
)
from .defs import ColDef
from .triggers import (
    get_table_triggers,
    CreateTrigger,
    DropTrigger,
    Trigger,
)

class DataFrame(abc.SQL):
    """
    A SQL analogue of pandas.DataFrame
    """
    def __init__(self, db, *, name=None, sql=None):
        if name is None and sql is None:
            raise TypeError("arguments 'name' and 'sql' cannot both be None.")
            
        if name is not None and sql is not None:
            raise TypeError("one of 'name' and 'sql' must be None.")
            
        self._db = db
        self._name = name
        if sql is not None:
            self._table = sql.subquery()
            self._sql = sql
    
    @property
    def db(self):
        return self._db
    
    @property
    def name(self):
        return self._name
    
    @property
    def table(self):
        return self._table if self.name is None else self.db.tables[self.name]
    
    @property
    def sql(self):
        return self._sql if self.name is None else sa.select(self.table)
    
    @property
    def columns(self):
        return tuple(c.name for c in self.table.c)
    
    @property
    def loc(self):
        return LocIndexer(self)
    
    @property
    def iloc(self):
        return ILocIndexer(self)
    
    @property
    def triggers(self):
        return DataFrameTriggers(self)
    
    def __len__(self):
        with self.db.connect() as con:
            return con.execute(sa.select(sa.func.count()).select_from(self.table)).fetchone()[0]
        
    def __contains__(self, key):
        return key in self.columns
    
    def __iter__(self):
        return self.columns
    
    def keys(self):
        return self.columns
    
    def items(self):
        for k in self.columns:
            yield k, self[k]
    
    def info(self):
        info = pd.DataFrame([{
            'column': c.name,
            'sql_type': c.type,
            'sqlalchemy_type': type(c.type).__name__,
            'default': c.server_default,
            'nullable': c.nullable,
            'unique': c.unique,
            'primary_key': c.primary_key,
            'foreign_keys': c.foreign_keys,
            'constraints': c.constraints,
            'autoincrement': c.autoincrement,
            'computed': c.computed,
        } for c in self.table.c])
        return info
        
    def __getitem__(self, key):
        if key is Ellipsis:
            col_key, row_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            col_key, row_key = key
        else:
            col_key, row_key = key, slice(None)
            
        if col_key is Ellipsis:
            col_key = slice(None)
            
        if row_key is Ellipsis:
            row_key = slice(None)
            
        if isinstance(col_key, str) and isinstance(row_key, int):
            result_class = Item
        elif isinstance(col_key, str):
            result_class = Column
        elif isinstance(row_key, int):
            result_class = Row
        else:
            result_class = DataFrame
            
        if isinstance(col_key, slice):
            if not (col_key.start is None and col_key.stop is None and col_key.step is None):
                raise ValueError(f"col_key can only be a slice if start, stop, and step are all None, but {col_key=}.")
            sql = sa.select(self.table)
        elif isinstance(col_key, str):
            sql = sa.select(self.table.c[col_key])
        elif isinstance(col_key, collections.abc.Iterable):
            sql = sa.select(*self.table.c[tuple(col_key)])
        else:
            raise TypeError(f"col_key must be a str, slice, Ellipsis, or Iterable, but {type(col_key)=}.")

        if isinstance(row_key, Column) and row_key.indexable:
            sql = sql.where(row_key.column)
        elif isinstance(row_key, int):
            if row_key < 0:
                raise ValueError(f"negative index not supported, but {row_key=}.")
            start, stop = row_key, row_key + 1
            sql = sql.slice(start, stop)
        elif isinstance(row_key, slice):
            if row_key.step is not None:
                raise ValueError(f"row_key can only be a slice if step is None, but {row_key=}.")
            if row_key.start is not None:
                if row_key.start < 0:
                    raise ValueError(f"negative index not supported, but {row_key.start=}.")
                sql = sql.offset(row_key.start)
            if row_key.stop is not None:
                if row_key.stop < 0:
                    raise ValueError(f"negative index not supported, but {row_key.stop=}.")
                sql = sql.limit(row_key.stop if row_key.start is None else row_key.stop - row_key.start)
        else:
            raise TypeError(f"row_key must be an indexable Column, int, slice, or Ellipsis, but {type(row_key)=}.")
            
        if result_class is Column:
            if isinstance(row_key, slice) and row_key.start is None and row_key.stop is None:
                return Column(self.db, column=self.table.c[col_key])
            col = Column(self.db, sql=sql)
            col.name = col_key
            return col
            
        return result_class(self.db, sql=sql)
    
    def __setitem__(self, key, value):
        if isinstance(value, ColDef):
            if not isinstance(key, str):
                raise TypeError(f"key must be a string if value is a ColDef, but {type(key)=}.")
            
            table = copy.deepcopy(self.table)
            column = sa.Column(key, *value.args, **value.kwargs)
            
            old_triggers = get_table_triggers(table)
            table.append_column(column)
            new_triggers = get_table_triggers(table)

            sql = alter.AddColumn(table.c[key])
            triggers = [trigger for trigger in new_triggers if trigger not in old_triggers]
            
            with self.db.connect() as con:
                con.execute(sql)
                for trigger in triggers:
                    con.execute(CreateTrigger(trigger))
                
            return
        
        if key is Ellipsis:
            col_key, row_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            col_key, row_key = key
        else:
            col_key, row_key = key, slice(None)
            
        if col_key is Ellipsis:
            col_key = slice(None)
            
        if row_key is Ellipsis:
            row_key = slice(None)
            
        if isinstance(value, abc.SQL):
            raise NotImplementedError()
            
        if isinstance(col_key, str):
            value = (value,)
        
        if isinstance(col_key, slice):
            if not (col_key.start is None and col_key.stop is None and col_key.step is None):
                raise ValueError(f"col_key can only be a slice if start, stop, and step are all None, but {col_key=}.")
            columns = self.columns
        elif isinstance(col_key, str):
            columns = (col_key,)
        elif isinstance(col_key, collections.abc.Iterable):
            columns = col_key
        else:
            raise TypeError(f"col_key must be a str, slice, Ellipsis, or Iterable, but {type(col_key)=}.")
            
        with self.db.connect() as con:
            # create new columns if necessary
            for column, v in zip(columns, value):
                if column not in self.columns:
                    self[column] = ColDef(types.infer_sqlalchemy_type(v))

            sql = sa.update(self.table)
        
            if isinstance(row_key, Column) and row_key.indexable:
                sql = sql.where(row_key.column)
            elif isinstance(row_key, int):
                raise NotImplementedError("Updating rows by row index is currently not supported")
            elif isinstance(row_key, slice):
                if not (row_key.start is None and row_key.stop is None and row_key.step is None):
                    raise ValueError(f"row_key can only be a slice if start, stop, and step are all None, but {row_key=}.")
                pass # update all rows
            else:
                raise TypeError(f"row_key must be an indexable Column, int, slice, or Ellipsis, but {type(row_key)=}.")
            
            sql = sql.values(dict(zip(columns, value)))
            con.execute(sql)
            
    def __delitem__(self, key):
        if key is Ellipsis:
            raise ValueError("key cannot be an Ellipsis since the deletion operation will be ambiguous.")
        elif isinstance(key, tuple):
            col_key, row_key = key
        else:
            col_key, row_key = key, Ellipsis
            
        if isinstance(col_key, slice) and not (col_key.start is None and col_key.stop is None and col_key.step is None):
            raise ValueError(f"col_key can only be a slice if start, stop, and step are all None, but {col_key=}.")
            
        if isinstance(row_key, slice) and not (row_key.start is None and row_key.stop is None and row_key.step is None):
            raise ValueError(f"row_key can only be a slice if start, stop, and step are all None, but {row_key=}.")
            
        if isinstance(col_key, slice) and isinstance(row_key, slice):
            raise ValueError(f"col_key and row_key cannot both be slices since the deletion operation will be ambiguous.")
            
        if col_key is Ellipsis and row_key is Ellipsis:
            raise ValueError(f"col_key and row_key cannot both be Ellipsis since the deletion operation will be ambiguous.")
           
        sqls = []
        if col_key is Ellipsis:
            if isinstance(row_key, Column) and row_key.indexable:
                sqls.append(sa.delete(self.table).where(row_key.column))
            elif isinstance(row_key, slice):
                sqls.append(sa.delete(self.table))
            else:
                raise NotImplementedError(f"row_key must be an indexable Column or a slice, but {row_key=}.")
            
        elif row_key is Ellipsis:
            if isinstance(col_key, str):
                col_key = [col_key]
            
            for c in col_key:
                sqls.append(alter.DropColumn(self.table.c[c]))
                
        else:
            raise ValueError("One of col_key or row_key must be an Ellipsis.")
            
        with self.db.connect() as con:
            for sql in sqls:
                con.execute(sql)
                
    def drop(self, index=None, columns=None):
        """
        I recommend using __delitem__ instead since it makes it clear that
        the modification is in place. This method is just for compatibility with pandas.
        """
        if index is None:
            index = Ellipsis
        if columns is None:
            columns = Ellipsis
            
        del self[columns, index]
        
        return self
        
    def rename(self, columns):
        sqls = [alter.RenameColumn(self.table.c[k], v) for k, v in columns.items()]
        
        with self.db.connect() as con:
            for sql in sqls:
                con.execute(sql)
                
        return self
                
    def to_html(self, max_rows=None, show_dimensions=False, formatters=None):
        """
        chatGPT-assisted code.
        """
        # perform everything in a single read transaction to prevent dataset from being modified during this process
        with self.db.connect() as con:
            N = len(self)
            columns = self.columns
            M = len(columns)
            
            if max_rows is None:
                max_rows = N
            else:
                max_rows = min(max_rows, N)

            if N <= max_rows:
                row_indices = [slice(None)]
            else:
                n_top = max_rows // 2
                n_bottom = max_rows - n_top
                row_indices = [slice(None, n_top)] + [-1] + [slice(N - n_bottom, None)]
                
            html_str = "<table><thead><tr>"
            html_str += "<th></th>"

            for column in columns:
                header = [html.escape(column)]
                html_str += f"<th>{'<br/>'.join(header)}</th>"
            html_str += "</tr></thead><tbody>"
                
            for indices in row_indices:
                if indices == -1:
                    html_str += "<tr>"
                    html_str += "<td>...</td>" * (M + 1)
                    html_str += "</tr>"
                elif isinstance(indices, slice):
                    data = self[:, indices].fetch()
                    indices = np.arange(N)[indices]
                    
                    for i, idx in enumerate(indices):
                        html_str += "<tr>"
                        html_str += f"<td><b>{idx}</b></td>"
                        for column in columns:
                            cell = data[column].iloc[i]
                            if formatters is not None and column in formatters:
                                cell = formatters[column](cell)
                            else:
                                cell = str(cell)

                            html_str += f"<td>{html.escape(cell)}</td>"
                        html_str += "</tr>"
                else:
                    raise RuntimeError()
                    
            html_str += "</tbody></table>"

            if show_dimensions:
                html_str += f"<p>{N} rows × {M} columns</p>"

            return html_str
        
    def _repr_html_(self):
        """
        For automatic pretty table rendering in jupyter by calling display(df)
        """
        
        return self.to_html(
            max_rows=options.display.max_rows,
            show_dimensions=options.display.show_dimensions,
        )

    def merge(self, df, how='inner', sort=False, on=None, left_on=None, right_on=None, suffixes=('_x', '_y'), indicator=False):
        left, right = self.table, df.table
        left_columns, right_columns = self.columns, df.columns
        
        if how == 'cross':
            if not on is None and left_on is None and right_on is None:
                raise ValueError(f"on, left_on, and right_on must all be None when how == 'cross', but {on=}, {left_on=}, {right_on=}.")
                
            overlap = [col for col in left_columns if col in right_columns]
            left_cols = [left.c[col].label(f'{col}{suffixes[0]}') if col in overlap else left.c[col] for col in left_columns]
            right_cols = [right.c[col].label(f'{col}{suffixes[1]}') if col in overlap else right.c[col] for col in right_columns]
            cols = [*left_cols, *right_cols]
            
            if indicator:
                cols.append(sa.literal('both').label('_merge'))
                
            sql = sa.select(*cols)
            
            return DataFrame(self.db, sql=sql)
        
        if on is not None:
            if not (left_on is None and right_on is None):
                raise ValueError(f"left_on and right_on must be None when on is not None, but {left_on=}, {right_on=}.")
            left_on, right_on = on, on
            
        if (left_on is None and right_on is not None) or (left_on is not None and right_on is None):
            raise ValueError(f"left_on and right_on must either be both None or not None, but {left_on=}, {right_on=}.")
        
        if left_on is None: # right_on must also be None
            on = [column for column in left_columns if column in right_columns] # same order as left df
            left_on, right_on = on, on
        else:
            left_on, right_on = np.atleast_1d(left_on), np.atleast_1d(right_on)
            if len(left_on) != len(right_on):
                raise ValueError(f"Length of left_on must be same as length of right_on, but {len(left_on)=}, {len(right_on)=}.")
                
        if sort:
            left = sa.select(left, sa.func.row_number().over().label('row_number')).subquery()
            right = sa.select(right, sa.func.row_number().over().label('row_number')).subquery()
        
        conds = ((left.c[lcol] == right.c[rcol]) | (left.c[lcol].is_(None) & right.c[rcol].is_(None)) for lcol, rcol in zip(left_on, right_on)) # SQL considers NA != NA, but pandas does when merging
        cond = functools.reduce(lambda x, y: x & y, conds)
        
        if how == 'inner':
            table = left.join(right, cond)
        elif how == 'left':
            table = left.join(right, cond, isouter=True)
        elif how == 'right': 
            table = right.join(left, cond, isouter=True)
        elif how == 'outer':
            table = left.join(right, cond, full=True)
        else:
            raise ValueError(f"how must be either 'inner', 'left', 'right', 'outer', or 'cross', but {how=}.")
            
        on = [lcol for lcol, rcol in zip(left_on, right_on) if lcol == rcol]
        
        left_cols = []
        for col in left_columns:
            if col in on:
                # if col is in on, then this is a column where the left and right columns
                # are merged into a single column. In this case, we want to make sure
                # that we take the non-null value if either the left or right value is null
                left_cols.append(
                    sa.case(
                        (left.c[col].is_(None), right.c[col]),
                        (right.c[col].is_(None), left.c[col]),
                        else_=left.c[col],
                    ).label(col)
                )
            elif col in right_columns:
                # has name conflict with right dataframe and is not an unambiguous column.
                # need 'col not in on' instead of 'col not in left_on' due to cases like
                # left_on=['a','b'], right_on=['b','a']
                left_cols.append(left.c[col].label(f'{col}{suffixes[0]}'))
            else:
                left_cols.append(left.c[col])
                
        right_cols = []
        for col in right_columns:
            if col in on:
                # if col is in on, then this is a column where the left and right columns
                # are merged into a single column. Since we already added this column to left_cols
                # we do not need to add it to right_cols as well.
                continue
            elif col in left_columns:
                # has name conflict with right dataframe and is not an unambiguous column.
                # need 'col not in on' instead of 'col not in left_on' due to cases like
                # left_on=['a','b'], right_on=['b','a']
                right_cols.append(right.c[col].label(f'{col}{suffixes[1]}'))
            else:
                right_cols.append(right.c[col])

        cols = [*left_cols, *right_cols]
        
        if indicator:
            if len(left_on) == 0:
                cols.append(sa.literal('both').label('_merge'))
                
            else:
                left_null = functools.reduce(lambda x, y: x & y, (c.is_(None) for c in left.c[tuple(left_on)]))
                right_null = functools.reduce(lambda x, y: x & y, (c.is_(None) for c in right.c[tuple(right_on)]))
                left_not_null = functools.reduce(lambda x, y: x | y, (c.isnot(None) for c in left.c[tuple(left_on)]))
                right_not_null = functools.reduce(lambda x, y: x | y, (c.isnot(None) for c in right.c[tuple(right_on)]))
                cols.append(
                    sa.case(
                        (left_null & right_not_null, 'right_only'),
                        (right_null & left_not_null, 'left_only'),
                        else_='both',
                    ).label('_merge')
                )
        
        if sort and how == 'outer':
            sql = sa.select(*cols, left.c.row_number.label('__left_row_number__'), right.c.row_number.label('__right_row_number__')).select_from(table)
        else:
            sql = sa.select(*cols).select_from(table)
        
        if sort:
            if how in ['inner', 'left']:
                sql = sql.order_by(*[left.c[col].nulls_last() for col in left_on], *[right.c[col].nulls_last() for col in right_on if col not in on], left.c.row_number, right.c.row_number)
            elif how == 'right':
                sql = sql.order_by(*[right.c[col].nulls_last() for col in right_on], *[left.c[col].nulls_last() for col in left_on if col not in on], right.c.row_number, left.c.row_number)
            elif how == 'outer':
                table = sql.subquery()
                left_on_cols = [table.c[f'{col}{suffixes[0]}' if (col not in on and col in right_columns) else col].nulls_last() for col in left_on]
                right_on_cols = [table.c[col if col not in left_columns else f'{col}{suffixes[1]}'].nulls_last() for col in right_on if col not in on]
                select_cols = [col for col in table.c if col.name not in ['__left_row_number__', '__right_row_number__']]
                sql = sa.select(*select_cols).order_by(*left_on_cols, *right_on_cols, table.c.__left_row_number__, table.c.__right_row_number__)
            else:
                raise RuntimeError("Not supposed to end up here.")
            
        return DataFrame(self.db, sql=sql)
    
    def sort_values(self, by, *, ascending=True):
        by = self.table.c[by].nulls_last()
        if not ascending:
            by = by.desc()
        return DataFrame(self.db, sql=sa.select(self.table).order_by(by))
    
    def groupby(self, columns):
        return DataFrameGroupBy(self, columns)
    
    def eval(self, condition, level=0):
        condition = parsing.preparse(condition)
        var_names = parsing.parse_var_names(condition)
        frame = sys._getframe(level+1) # see https://github.com/pandas-dev/pandas/blob/main/pandas/core/computation/scope.py
        env = frame.f_globals | frame.f_locals
        
        # add @ variables
        var_dict = {f'{parsing.LOCAL_TAG}{k}': env[k] for k in var_names}
        
        # add dataframe columns
        var_dict = var_dict | {parsing.clean_column_name(k): v for k, v in self.items() if not isinstance(k, int)}
        
        return eval(condition, var_dict)
    
    def query(self, condition, level=0):
        return self[:,self.eval(condition, level=level+1)]
    
    def append(self, obj, execute=True):
        if isinstance(obj, pd.DataFrame):
            obj = obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            obj = obj.to_dict()
                
        sql = sa.insert(self.table).values(obj)
            
        if execute:
            with self.db.connect() as con:
                con.execute(sql)
        else:
            return sql
            
            
class LocIndexer:
    def __init__(self, df):
        self.df = df
        
    def __getitem__(self, key):
        if key is Ellipsis:
            row_key, col_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            row_key, col_key = key
        else:
            row_key, col_key = key, slice(None)
            
        if isinstance(row_key, slice) and row_key.stop is not None:
            # pd.Dataframe.loc has the HORRIBLE behavior that slicing INCLUDES the endpoint
            row_key = slice(row_key.start, row_key.stop + 1, row_key.step)
            
        return self.df[col_key, row_key]
    
    def __setitem__(self, key, value):
        if key is Ellipsis:
            row_key, col_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            row_key, col_key = key
        else:
            row_key, col_key = key, slice(None)
            
        if isinstance(row_key, slice) and row_key.stop is not None:
            # pd.Dataframe.loc has the HORRIBLE behavior that slicing INCLUDES the endpoint
            row_key = slice(row_key.start, row_key.stop + 1, row_key.step)
            
        self.df[col_key, row_key] = value
        
        
class ILocIndexer:
    def __init__(self, df):
        self.df = df
        
    def __getitem__(self, key):
        if key is Ellipsis:
            row_key, col_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            row_key, col_key = key
        else:
            row_key, col_key = key, slice(None)
            
        return self.df[col_key, row_key]
    
    def __setitem__(self, key, value):
        if key is Ellipsis:
            row_key, col_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            row_key, col_key = key
        else:
            row_key, col_key = key, slice(None)
            
        self.df[col_key, row_key] = value
        
        
class DataFrameTriggers(collections.UserDict):
    def __init__(self, df):
        db = df.db
        
        if not db.backend == 'sqlite':
            raise NotImplementedError(f"DataFrameTriggers is currently only tested for SQLite, but {db.backend=}.")

        self.df = df
        self.db = db
        self.data = self._fetch_data()
        
    def _fetch_data(self):
        with self.db.connect() as con:
            rows = con.execute(sa.text(f"SELECT sql FROM sqlite_master WHERE type = 'trigger' AND tbl_name = '{self.df.name}'")).fetchall()
        triggers = (Trigger.from_sql(self.db, row[0]) for row in rows)
        return {trigger.name: trigger for trigger in triggers}
        
    def __setitem__(self, key, value):
        value.name = key
        with self.db.connect() as con:
            con.execute(CreateTrigger(value))
            self.data = self._fetch_data()
            
    def __delitem__(self, key):
        with self.db.connect() as con:
            con.execute(DropTrigger(key))
            self.data = self._fetch_data()
            
    def __str__(self):
        s = ', '.join(f'{k}: {str(v)}' for k, v in self.data.items())
        return f'{{{s}}}'
    
class DataFrameGroupBy:
    def __init__(self, df, columns):
        self.df = df
        self.columns = tuple(columns)
        self.ungrouped_columns = tuple(col for col in self.df.columns if col not in self.columns)
    
    def __getitem__(self, key):
        if not isinstance(key, str):
            raise NotImplementedError(f"Currently only supports string key, but {key=}.")
        return ColumnGroupBy(self, key)
    
    @property
    def groups(self):
        return DataFrame(self.df.db, sql=sa.select(*self.df.table.c[self.columns]).group_by(*self.columns))
    
    @property
    def nth(self):
        return GroupByNthSelector(self)
    
    def get_group(self, key):
        if isinstance(key, str):
            key = (key,)
        if isinstance(key, collections.abc.Iterable):
            key = (k.item() if isinstance(k, np.generic) else k for k in key) # need to convert possibly numpy dtypes to native python types
        conditions = (self.df.table.c[column] == k for column, k in zip(self.columns, key))
        condition = functools.reduce(lambda x, y: x & y, conditions)
        return DataFrame(self.df.db, sql=sa.select(self.df.table).where(condition))
    
    def agg(self, *args, **kwargs):
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                new_args += [(col, arg) for col in self.ungrouped_columns]
            elif isinstance(arg, tuple):
                new_args.append(arg)
            else:
                raise TypeError(f"arg must be a string or a 2-tuple, but {arg=}.")
        args = new_args
        
        columns = []
        for k, v in itertools.chain(zip(args, args), kwargs.items()):
            k = f'{k[0]}_{k[1]}' if isinstance(k, tuple) else k
            column, func = v
                
            if func == 'nunique':
                column = sa.func.count(self.df.table.c[column].distinct()).label(k)
                
            else:
                if func == 'mean':
                    func = 'avg'
                column = getattr(sa.func, func)(self.df.table.c[column]).label(k)
                
            columns.append(column)
        
        return DataFrame(self.df.db, sql=sa.select(*self.df.table.c[self.columns], *columns).group_by(*self.columns))
        
    def transform(self, *args, **kwargs):
        raise NotImplementedError()
        
    def nunique(self):
        return DataFrame(self.df.db, sql=sa.select(*self.df.table.c[self.columns], *[sa.func.count(self.df.table.c[col].distinct()).label(col) for col in self.ungrouped_columns]).group_by(*self.columns))
    
    def count(self):
        return self.agg('count')
    
    def sum(self):
        return self.agg('sum')
    
    def mean(self):
        return self.agg('mean')
    
class GroupByNthSelector:
    def __init__(self, gb):
        self.gb = gb
        
    def __getitem__(self, key):
        df = sa.select(self.gb.df.table, sa.func.row_number().over(partition_by=self.gb.columns).label('row_number'), sa.func.row_number().over().label('order')).subquery()
        
        where = df.c.row_number
        
        if isinstance(key, int):
            where = where == (key + 1)
        elif isinstance(key, slice):
            if key.start is not None:
                if key.start < 0:
                    raise ValueError(f"negative index not supported, but {key.start=}.")
                where = where >= (key.start + 1)
            if key.stop is not None:
                if key.stop < 0:
                    raise ValueError(f"negative index not supported, but {key.stop=}.")
                where = where < (key.stop + 1)
        else:
            raise KeyError(f"key must be an int or a slice, but {type(key)=}.")
            
        return DataFrame(self.gb.df.db, sql=sa.select(*df.c[self.gb.df.columns]).where(where).order_by(df.c.order))
    
    
class ColumnGroupBy:
    def __init__(self, gb, column):
        self.gb = gb
        self.column = column
        
    def nunique(self):
        return Column(self.gb.df.db, sql=sa.select(sa.func.count(self.gb.df.table.c[self.column].distinct())).group_by(*self.gb.columns))
    
    def count(self):
        return self.agg('count')
    
    def sum(self):
        return self.agg('sum')
    
    def mean(self):
        return self.agg('mean')
 
    def agg(self, *args, **kwargs):
        N = len(args) + len(kwargs)
        
        columns = []
        for v in itertools.chain(args, kwargs.items()):
            if isinstance(v, tuple):
                k, v = v
            else:
                k = self.column if N == 1 else v
            
            if v == 'nunique':
                column = sa.func.count(self.gb.df.table.c[self.column].distinct()).label(k)
            
            else:
                if v == 'mean':
                    v = 'avg'
                column = getattr(sa.func, v)(self.gb.df.table.c[self.column]).label(k)
                
            columns.append(column)

        if N == 1:
            return Column(self.gb.df.db, sql=sa.select(*columns).group_by(*self.gb.columns))
        
        return DataFrame(self.gb.df.db, sql=sa.select(*self.gb.df.table.c[self.gb.columns], *columns).group_by(*self.gb.columns))
    
    def transform(self, *args, **kwargs):
        columns = []
        for v in itertools.chain(args, kwargs.items()):
            k, v = v if isinstance(v, tuple) else (v, v)
                
            if v == 'nunique':
                column = sa.func.count(self.gb.df.table.c[self.column].distinct())
            
            else:
                if v == 'mean':
                    v = 'avg'
                column = getattr(sa.func, v)(self.gb.df.table.c[self.column])
            
            column = column.over(partition_by=self.gb.columns).label(k)
            columns.append(column)
            
        result_class = Column if len(columns) == 1 else DataFrame
        
        return result_class(self.gb.df.db, sql=sa.select(*columns).order_by(sa.func.row_number().over()))
    
    
@lib.functools.parametrized
def _column_method(func, cls=None, autocast=True, autoname=True):
    @functools.wraps(func)
    def wrapped(self, *args):
        nonlocal cls
        
        if cls is None:
            cls = Column
        elif isinstance(cls, str):
            cls = globals()[cls] # allow passing string since sometimes we need to pass the class before it is initialized, as in JSONMethods.__getitem__
            
        indexable = self.indexable and all(arg.indexable for arg in args if isinstance(arg, Column))
        is_array = self.is_array and all(arg.is_array for arg in args if isinstance(arg, Column))

        expr = self.column if indexable else self.sql

        if autocast and len(args) == 1 and isinstance(self, JSONMethods):
            arg = args[0]
            if isinstance(arg, str):
                expr = expr.as_string()
            elif isinstance(arg, bool):
                expr = expr.as_boolean() # need to check bool before int since bool is a sublcass of int
            elif isinstance(arg, int):
                expr = expr.as_integer()
            elif isinstance(arg, float):
                expr = expr.as_float()
            elif isinstance(arg, numbers.Number):
                expr = expr.as_numeric()
            else:
                raise TypeError(f"JSON currently only supports binary expressions involving one of [str, bool, int, float, numbers.Number], but got value {arg} with type {type(arg)}.")

        expr = func(expr, *(arg if not isinstance(arg, Column) else arg.column if indexable else arg.sql for arg in args))

        if indexable:
            col = cls(self.db, column=expr, is_array=is_array)
        else:
            col = cls(self.db, sql=expr, is_array=is_array)
    
        if autoname:
            if all(arg.name == self.name for arg in args if isinstance(arg, Column)):
                col.name = self.name
            else:
                col.name = None
        
        return col

    return wrapped
    

class Column(abc.SQL):
    def __init__(self, db, *, column=None, sql=None, is_array=False):
        if column is None and sql is None:
            raise TypeError("arguments 'column' and 'sql' cannot both be None.")
            
        if column is not None and sql is not None:
            raise TypeError("one of 'column' and 'sql' must be None.")
            
        self._db = db
        self._indexable = sql is None
        self._sql = sa.select(column) if sql is None else sql
        self._column = sql.subquery() if column is None else column
        self._is_array = is_array
        self.name = getattr(column, 'name', None)
        
    def fetch(self, **kwargs):
        df = super().fetch(**kwargs)
        s = next(df.items())[1].rename(self.name)
        if self.is_array:
            if isinstance(s.dtype, pd.api.extensions.ExtensionDtype):
                s = s.array
            else:
                s = s.to_numpy()
        return s
    
    @property
    def db(self):
        return self._db
    
    @property
    def sql(self):
        return self._sql
    
    @property
    def column(self):
        return self._column
    
    @property
    def indexable(self):
        return self._indexable
    
    @property
    def is_array(self):
        return self._is_array
    
    @property
    def str(self):
        if not isinstance(self.column.type, sa.types.Text):
            raise TypeError(f"'str' methods only apply to Text columns, but {self.column.type=}.")
        if self.indexable:
            return StringMethods(self.db, column=self.column)
        return StringMethods(self.db, sql=self.sql)
    
    @property
    def json(self):
        if not isinstance(self.column.type, sa.types.JSON):
            raise TypeError(f"'json' methods only apply to JSON columns, but {self.column.type=}.")
        
        if self.indexable:
            return JSONMethods(self.db, column=self.column)
        return JSONMethods(self.db, sql = self.sql)
    
    @_column_method()
    def isna(self):
        return self.is_(None)
    
    def isnull(self):
        return self.isna()
    
    def max(self):
        return Item(self.db, sa.select(sa.func.max(self.column)))
    
    def min(self):
        return Item(self.db, sa.select(sa.func.min(self.column)))
    
    def any(self):
        if not isinstance(self.column.type, sa.Boolean):
            raise TypeError("any() not supported for non-boolean columns.")
        return self.max() # SQLite does not support any
    
    def all(self):
        if not isinstance(self.column.type, sa.Boolean):
            raise TypeError("any() not supported for non-boolean columns.")
        return self.min() # SQLite does not support all
    
    def unique(self):
        return Column(self.db, sql=sa.select(self.column.distinct()), is_array=True)
    
    def nunique(self):
        return Item(self.db, sql=sa.select(sa.func.count(self.column.distinct())))
    
    @_column_method()
    def isin(self, x):
        if not isinstance(x, collections.abc.Container):
            raise TypeError(f"The operator 'isin' only applies to container types, but {type(x)=}.")
            
        return self.in_(x)
    
    @_column_method()
    def __add__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '+' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '+' is only valid for numbers and booleans, but {type(x)=}.")
        
        type_ = self.type
        if isinstance(x, sa.ColumnElement):
            type_ = types.result_sql_type(type_, x.type)
        return (self + x).cast(type_)
    
    @_column_method()
    def __sub__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '-' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '-' is only valid for numbers and booleans, but {type(x)=}.")
        
        type_ = self.type
        if isinstance(x, sa.ColumnElement):
            type_ = types.result_sql_type(type_, x.type)
        return (self - x).cast(type_)
    
    @_column_method()
    def __mul__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '*' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '*' is only valid for numbers and booleans, but {type(x)=}.")
        
        type_ = self.type
        if isinstance(x, sa.ColumnElement):
            type_ = types.result_sql_type(type_, x.type)
        return (self * x).cast(type_)
    
    @_column_method()
    def __truediv__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '/' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '/' is only valid for numbers and booleans, but {type(x)=}.")
        
        if isinstance(self.type, sa.Integer) and (not isinstance(x, sa.ColumnElement) or isinstance(x.type, sa.Integer)):
            type_ = sa.Double() # use double if neither self nor x is a floating-point column 
        else:
            type_ = self.type
            if isinstance(x, sa.ColumnElement):
                type_ = types.result_sql_type(type_, x.type)
        return (self / x).cast(type_)
    
    @_column_method()
    def __floordiv__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '//' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '//' is only valid for numbers and booleans, but {type(x)=}.")
        
        type_ = self.type
        if isinstance(x, sa.ColumnElement):
            type_ = types.result_sql_type(type_, x.type)
        
        if isinstance(self.type, sa.Numeric) or (isinstance(x, sa.ColumnElement) and isinstance(x.type, sa.Numeric)):
            # need to do this due to SQLite bug that crashes when one of the columns is a float and has NaNs.
            cond = self.is_(None)
            if isinstance(x, sa.ColumnElement):
                cond = cond | x.is_(None)
                
            return sa.case((cond, None), else_=self // x).cast(type_)

        return (self // x).cast(type_)
    
    @_column_method()
    def __pow__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '**' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '**' is only valid for numbers and booleans, but {type(x)=}.")
        
        # First, handle the case where the result can be an integer
        if isinstance(self.type, sa.Integer):
            if isinstance(x, (int, np.integer)) and x >= 0:
                return sa.func.pow(self, x).cast(self.type)
            elif isinstance(x, sa.ColumnElement) and isinstance(x.type, sa.Integer):
                return sa.case(
                    (x >= 0, sa.func.pow(self, x).cast(types.result_sql_type(self.type, x.type))),
                    else_=sa.func.pow(self, x).cast(sa.Double()),
                )
            else:
                return sa.func.pow(self, x).cast(sa.Double())
            
        type_ = self.type
        if isinstance(x, sa.ColumnElement):
            type_ = types.result_sql_type(type_, x.type)
            
        return sa.func.pow(self, x).cast(type_)
    
    @_column_method()
    def __mod__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '%' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '%' is only valid for numbers and booleans, but {type(x)=}.")
        
        if isinstance(self.type, sa.Numeric) or isinstance(x, (float, np.floating)) or (isinstance(x, sa.ColumnElement) and isinstance(x.type, sa.Numeric)):
            raise TypeError("The operator '%' currently does not support floats.") # due to sqlite limitation
        
        type_ = types.result_sql_type(self.type, sa.SmallInteger())
        if isinstance(x, sa.ColumnElement):
            type_ = types.result_sql_type(type_, x.type)
        return (self % x).cast(type_)
    
    @_column_method()
    def __and__(self, x):
        if not (isinstance(self.type, sa.Boolean) and (isinstance(x, (bool, np.bool_)) or (isinstance(x, sa.ColumnElement) and isinstance(x.type, sa.Boolean)))):
            # note: for integer columns SQL will return a sensible answer (treating integers != 0 as True and otherwise False)
            # but pandas will first convert integer to binary and then perform bitwise-and, which I don't think makes sense,
            # since bitwise-and should mean element-wise and, not element-wise bitwise-and. So I just forbid bitwise-and
            # on integer columns for now to prevent confusion.
            raise TypeError("The operator '&' is only valid for booleans.")
        if isinstance(x, (bool, np.bool_)) and x is False:
            x = sa.literal(x) # sqlalchemy bug, it returns a single False instead of a column of False when x is False
        return self & x
    
    @_column_method()
    def __or__(self, x):
        if not (isinstance(self.type, sa.Boolean) and (isinstance(x, (bool, np.bool_)) or (isinstance(x, sa.ColumnElement) and isinstance(x.type, sa.Boolean)))):
            # note: see explanation in the method __and__
            raise TypeError("The operator '|' is only valid for booleans.")
        if isinstance(x, (bool, np.bool_)) and x is True:
            x = sa.literal(x) # sqlalchemy bug, it returns a single True instead of a column of True when x is True
        return self | x
    
    @_column_method()
    def __xor__(self, x):
        if not (isinstance(self.type, sa.Boolean) and (isinstance(x, (bool, np.bool_)) or (isinstance(x, sa.ColumnElement) and isinstance(x.type, sa.Boolean)))):
            # note: see explanation in the method __and__
            raise TypeError("The operator '^' is only valid for booleans.")
        return self ^ x
    
    @_column_method()
    def __radd__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '+' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '+' is only valid for numbers and booleans, but {type(x)=}.")

        return (self + x).cast(self.type)
    
    @_column_method()
    def __rsub__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '-' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '-' is only valid for numbers and booleans, but {type(x)=}.")
            
        return (x - self).cast(self.type)
    
    @_column_method()
    def __rmul__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '*' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '*' is only valid for numbers and booleans, but {type(x)=}.")
            
        return (x * self).cast(self.type)
    
    @_column_method()
    def __rtruediv__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '/' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '/' is only valid for numbers and booleans, but {type(x)=}.")
            
        if isinstance(self.type, sa.Integer):
            type_ = sa.Double() # use double if neither self nor x is a floating-point column 
        else:
            type_ = self.type
        return (x / self).cast(type_)
    
    @_column_method()
    def __rfloordiv__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '//' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '//' is only valid for numbers and booleans, but {type(x)=}.")
        
        if isinstance(self.type, sa.Numeric):
            # need to do this due to SQLite bug hat crashes when columns are floats and has NaNs.
            return sa.case(
                (self.is_(None), None),
                else_=x // self,
            ).cast(self.type)
        return (x // self).cast(self.type)
    
    @_column_method()
    def __rpow__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '**' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '**' is only valid for numbers and booleans, but {type(x)=}.")
            
        # First, handle the case where the result can be an integer
        if isinstance(self.type, sa.Integer):
            if isinstance(x, (int, np.integer)):
                return sa.case(
                    (self >= 0, sa.func.pow(x, self).cast(self.type)),
                    else_=sa.func.pow(x, self).cast(sa.Double()),
                )
            else:
                return sa.func.pow(x, self).cast(sa.Double())

        return sa.func.pow(x, self).cast(self.type)
    
    @_column_method()
    def __rmod__(self, x):
        if not isinstance(self.type, (sa.Numeric, sa.Integer, sa.Boolean)):
            raise TypeError(f"The operator '%' is only valid for numbers and booleans, but {self.type=}.")
        if not isinstance(x, (sa.Column, sa.Label, numbers.Number, bool, np.bool_)):
            raise TypeError(f"The operator '%' is only valid for numbers and booleans, but {type(x)=}.")
            
        if isinstance(self.type, sa.Numeric) or isinstance(x, (float, np.floating)):
            raise TypeError("The operator '%' currently does not support floats.") # due to sqlite limitation
        
        type_ = types.result_sql_type(self.type, sa.SmallInteger())
        return (x % self).cast(type_)
    
    @_column_method()
    def __rand__(self, x):
        if not (isinstance(self.type, sa.Boolean) and isinstance(x, (bool, np.bool_))):
            # note: see explanation in the method __and__
            raise TypeError("The operator '&' is only valid for booleans.")
        if isinstance(x, (bool, np.bool_)) and x is False:
            x = sa.literal(x) # sqlalchemy bug, it returns a single False instead of a column of False when x is False
        return self & x # sqlalchemy does not have __rand__, probably since & is symmetric anyway
    
    @_column_method()
    def __ror__(self, x):
        if not (isinstance(self.type, sa.Boolean) and isinstance(x, (bool, np.bool_))):
            # note: see explanation in the method __and__
            raise TypeError("The operator '|' is only valid for booleans.")
        if isinstance(x, (bool, np.bool_)) and x is True:
            x = sa.literal(x) # sqlalchemy bug, it returns a single False instead of a column of False when x is False
        return self | x # sqlalchemy does not have __ror__, probably since & is symmetric anyway
    
    @_column_method()
    def __rxor__(self, x):
        if not (isinstance(self.type, sa.Boolean) and isinstance(x, (bool, np.bool_))):
            # note: see explanation in the method __and__
            raise TypeError("The operator '^' is only valid for booleans.")
        return x ^ self
    
    @_column_method()
    def __eq__(self, x):
        return self == x
    
    @_column_method()
    def __ne__(self, x):
        return self != x
    
    @_column_method()
    def __lt__(self, x):
        if isinstance(x, (bool, np.bool_)):
            x = int(x) # need to do this since sqlalchemy does not allow inequality comparison with bool
        return self < x
    
    @_column_method()
    def __le__(self, x):
        if isinstance(x, (bool, np.bool_)):
            x = int(x) # need to do this since sqlalchemy does not allow inequality comparison with bool
        return self <= x
    
    @_column_method()
    def __gt__(self, x):
        if isinstance(x, (bool, np.bool_)):
            x = int(x) # need to do this since sqlalchemy does not allow inequality comparison with bool
        return self > x
    
    @_column_method()
    def __ge__(self, x):
        if isinstance(x, (bool, np.bool_)):
            x = int(x) # need to do this since sqlalchemy does not allow inequality comparison with bool
        return self >= x
    
    @_column_method()
    def __neg__(self):
        if not isinstance(self.type, (sa.Integer, sa.Numeric)):
            raise TypeError(f"The unary operator '-' only applies to numeric data types, but {self.type=}.")
        return -self
    
    @_column_method()
    def __pos__(self):
        if not isinstance(self.type, (sa.Integer, sa.Numeric)):
            raise TypeError(f"The unary operator '+' only applies to numeric data types, but {self.type=}.")
        return self
    
    @_column_method()
    def __invert__(self):
        if not isinstance(self.type, sa.Boolean):
            raise TypeError(f"The unary operator '~' only applies to booleans, but {self.type=}.")
        return ~self
    

class StringMethods(Column):
    @_column_method()
    def contains(self, pat):
        if not isinstance(pat, str):
            raise TypeError(f"The operator 'str.contains' only applies to str, but {type(pat)=}.")
            
        return self.like(f'%{pat}%')
    
    @_column_method()
    def startswith(self, pat):
        if not isinstance(pat, str):
            raise TypeError(f"The operator 'str.endswith' only applies to str, but {type(pat)=}.")
            
        return self.like(f'{pat}%')
    
    @_column_method()
    def endswith(self, pat):
        if not isinstance(pat, str):
            raise TypeError(f"The operator 'str.endswith' only applies to str, but {type(pat)=}.")
            
        return self.like(f'%{pat}')
    
    
class JSONMethods(Column):
    @_column_method(cls='JSONMethods', autocast=False, autoname=False)
    def __getitem__(self, key):
        column = self[key]
        column.name = f'{self.name}.{str(key)}'
        return column
    
      
class Row(abc.SQL):
    def fetch(self, **kwargs):
        df = super().fetch(**kwargs)
        return df.iloc[0]
    

class Item(abc.SQL):
    def fetch(self, **kwargs):
        df = super().fetch(**kwargs)
        return df.iloc[0][0]