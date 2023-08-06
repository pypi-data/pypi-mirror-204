import contextlib
import warnings
import logging

import sqlalchemy as sa
import pandas as pd
import hyclib as lib

from . import (
    options,
    types,
    get_table_triggers,
    alter,
    TableDef,
)
from .dataframe import DataFrame

logger = logging.getLogger(__name__)

__all__ = ['Database']

@lib.clstools.attr_repr
class Database:
    def __init__(self, **kwargs):
        kwargs = options.db | kwargs
        
        url_keys = [
            'drivername',
            'username',
            'password',
            'host',
            'port',
            'database',
            'query',
        ]
        url_kwargs = {k: kwargs.pop(k) for k in url_keys if k in kwargs}
            
        self._engine = sa.create_engine(sa.URL.create(**url_kwargs), **kwargs)
        self._metadata = sa.MetaData()
        self._connection = None
        
        if self.backend == 'sqlite':
            with self.connect() as con:
                con.execute(sa.text('PRAGMA case_sensitive_like=ON'))
        else:
            warnings.warn("Case sensitive search currently not gauaranteed for dialects other than sqlite.")
            
        if self.backend == 'sqlite':
            # python sqlite3 transaction handling does NOT work for DDL statements like CREATE and ALTER TABLE
            # See link: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-serializable
            @sa.event.listens_for(self.engine, "connect")
            def do_connect(dbapi_connection, connection_record):
                # disable pysqlite's emitting of the BEGIN statement entirely.
                # also stops it from emitting COMMIT before any DDL.
                dbapi_connection.isolation_level = None

            @sa.event.listens_for(self.engine, "begin")
            def do_begin(conn):
                # emit our own BEGIN
                conn.exec_driver_sql("BEGIN")
                
        @sa.event.listens_for(sa.Table, "column_reflect")
        def _setup_types(inspector, table, column_info):
            if isinstance(column_info["type"], sa.LargeBinary):
                # PickleType is not a SQL type and thus does not persist across different db.Database instances.
                # So we just assume all blobs are pickletypes, which should be a reasonable assumption.
                # See link: https://docs.sqlalchemy.org/en/20/core/custom_types.html#custom-and-decorated-types-reflection
                column_info["type"] = sa.PickleType()
            # elif isinstance(column_info["type"] ,sa.Numeric):
            #     # by default, numeric data types are returned as decimal.Decimal objects,
            #     # which is almost never used in typical pandas dataframes,
            #     # so we disable conversion to decimal.Decimal objects
            #     column_info["type"] = sa.Numeric(asdecimal=False)
                
    @property
    def engine(self):
        return self._engine
    
    @property
    def connection(self):
        return self._connection
                
    @property
    def dialect(self):
        return self.engine.dialect
            
    @property
    def backend(self):
        return self.engine.dialect.name
        
    @property
    def metadata(self):
        # Note: ideally we could just call self._metadata.reflect(con).
        # Unfortunately, metadata.reflect(con) only adds new tables and
        # does not remove tables or alter tables.
        
        # get new metadata
        new_metadata = sa.MetaData()
        
        # Reflection picks up the UPPERCASE data types that is backend-specific, which is undersirable.
        # So we convert it to a backend-agnostic, CamelCase datatype.
        # See link: https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-dbagnostic-types
        @sa.event.listens_for(new_metadata, "column_reflect")
        def genericize_datatypes(inspector, tablename, column_dict):
            column_dict["type"] = column_dict["type"].as_generic()
                
        with self.connect() as con:
            new_metadata.reflect(con)
        
        modified = False
        try:
            # modified if one of the table has a new schema
            for _, old_table, new_table in lib.itertools.dict_zip(self._metadata.tables, new_metadata.tables, mode='strict'):
                old_schema = str(sa.schema.CreateTable(old_table).compile(self.engine))
                new_schema = str(sa.schema.CreateTable(new_table).compile(self.engine))
                if old_schema != new_schema:
                    modified = True
                    
        except (KeyError, ValueError):
            # modified if table added, renamed, or dropped
            modified = True
            
        # If modified, use new_metadata to ensure we have the most updated tables.
        # Otherwise, keep using the same metadata so sqlalchemy understands that
        # the tables obtained from different calls to self.metadata.tables are the same
        if modified:
            logger.debug("Replaced metadata.")
            self._metadata = new_metadata
            
        return self._metadata
        
    @property
    def tables(self):
        return self.metadata.tables
    
    def keys(self):
        return self.tables.keys()
    
    def values(self):
        return self.tables.values()
    
    def items(self):
        return self.tables.items()
        
    def __enter__(self):
        self._connection = self.engine.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.commit() # commit only if there is no error
        self.connection.close()
        
    @contextlib.contextmanager
    def connect(self):
        if self.connection is None:
            try:
                self._connection = self.engine.connect()
                yield self.connection
            except Exception as err:
                raise err
            else:
                self.connection.commit() # commit only if there is no error
            finally:
                self.connection.close()
                self._connection = None
        else:
            # already connected inside a with-statement, so no need to call connect() and close().
            # also do not call commit() to pass transaction control to the top-level with-statement
            try:
                yield self.connection
            except Exception as err:
                raise err
            finally:
                pass
        
    def __getitem__(self, key):
        return DataFrame(self, name=key)
    
    def __setitem__(self, key, value):
        if isinstance(value, TableDef):
            with self.connect() as con:
                metadata = self.metadata
                table = sa.Table(key, metadata, *value.args, **value.kwargs)
                metadata.create_all(con)
                triggers = get_table_triggers(table)
                for trigger in triggers:
                    con.execute(trigger)
        elif isinstance(value, pd.DataFrame):
            index = value.index
            if not isinstance(index, pd.RangeIndex) or index.start != 0 or index.stop != len(value) or index.step != 1:
                raise ValueError(f"dataframe must have default range index, since SQL databases do not support indices, but {index=}.")
            categorical_columns = [k for k in value.columns if value.dtypes[k] == "category"]
            if len(categorical_columns) > 0:
                warnings.warn("Converting categorical columns to object dtypes since SQL does not support categorical columns.")
            value = value.astype({k: 'object' for k in categorical_columns})
            dtype = {k: types.infer_sqlalchemy_type(v) for k, v in value.items()}
            with self.connect() as con:
                value.to_sql(key, con=con, if_exists='replace', index=False, dtype=dtype)
        else:
            raise TypeError(f"value must be dfdb.TableDef or pd.DataFrame, but {type(value)=}.")
            
    def __delitem__(self, key):
        with self.connect() as con:
            self.tables[key].drop(con)
            
    def rename(self, old, new):
        with self.connect() as con:
            con.execute(alter.RenameTable(self.tables[old], new))
            
    def __contains__(self, key):
        return key in self.tables

    def __str__(self):
        return lib.pprint.pformat({k: repr(v) for k, v in self.items()}, verbose=True)