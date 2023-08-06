from sqlalchemy import literal
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement, CreateColumn

__all__ = ['AddColumn', 'DropColumn', 'RenameColumn', 'RenameTable']

class AddColumn(DDLElement):
    inherit_cache = False

    def __init__(self, column):
        self.table = column.table
        self.column = CreateColumn(column)

@compiles(AddColumn)
def visit_add_column(element, ddlcompiler, **kw):
    kw['literal_binds'] = True
    sql_compiler = ddlcompiler.sql_compiler
    
    table = sql_compiler.process(element.table, asfrom=True, **kw)
    column = ddlcompiler.process(element.column, **kw)
    return f"ALTER TABLE {table} ADD COLUMN {column}"

class DropColumn(DDLElement):
    inherit_cache = False

    def __init__(self, column):
        self.table = column.table
        self.column = column

@compiles(DropColumn)
def visit_drop_column(element, ddlcompiler, **kw):
    kw['literal_binds'] = True
    sql_compiler = ddlcompiler.sql_compiler
    
    table = sql_compiler.process(element.table, asfrom=True, **kw)
    column_name = sql_compiler.process(literal(str(element.column.name)), **kw)
    return f"ALTER TABLE {table} DROP COLUMN {column_name}"

class RenameColumn(DDLElement):
    inherit_cache = False
    
    def __init__(self, column, name):
        self.table = column.table
        self.column = column
        self.name = name
    
@compiles(RenameColumn)
def visit_rename_column(element, ddlcompiler, **kw):
    kw['literal_binds'] = True
    sql_compiler = ddlcompiler.sql_compiler
    
    table = sql_compiler.process(element.table, asfrom=True, **kw)
    old_name = sql_compiler.process(literal(str(element.column.name)), **kw)
    new_name = sql_compiler.process(literal(element.name), **kw)
    return f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name}"

class RenameTable(DDLElement):
    inherit_cache = False
    
    def __init__(self, table, name):
        self.table = table
        self.name = name
        
@compiles(RenameTable)
def visit_rename_table(element, ddlcompiler, **kw):
    kw['literal_binds'] = True
    sql_compiler = ddlcompiler.sql_compiler
    
    table = sql_compiler.process(element.table, asfrom=True, **kw)
    name = sql_compiler.process(literal(element.name), **kw)
    return f"ALTER TABLE {table} RENAME TO {name}"