import sqlalchemy as sa
from sqlalchemy.sql.expression import ClauseElement
import hyclib as lib

__all__ = ['TableDef', 'ColDef']

@lib.clstools.attr_repr
class TableDef:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return repr(sa.Table('__notset__', sa.MetaData(), *self.args, **self.kwargs))

@lib.clstools.attr_repr
class ColDef:
    """
    Same as sqlalchemy.Column, except there is no 'name' argument.
    See https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.__init__
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise TypeError("Must provide column type as the first argument.")
            
        self.args = args
        type_ = args[0]
        
        if 'server_default' in kwargs:
            server_default = kwargs['server_default']
            if not isinstance(server_default, ClauseElement):
                if not isinstance(server_default, type_.python_type):
                    raise TypeError(f"{type(server_default)=} does not match the python type ({type_.python_type}) of the column.")
                server_default = sa.text(str(server_default))
            kwargs['server_default'] = server_default
            
        self.kwargs = kwargs
        
    def __str__(self):
        return repr(sa.Column('__notset__', *self.args, **self.kwargs))