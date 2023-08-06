import uuid
import functools
import re

from sqlalchemy import update, text, literal
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql.expression import FromClause, ColumnElement, ColumnCollection

import hyclib as lib

__all__ = ['Trigger', 'CreateTrigger', 'DropTrigger', 'get_table_triggers']

def get_table_triggers(table):
    triggers = []
    for column in table.c:
        if column.server_onupdate is not None:
            pks = tuple(table.primary_key)
            if len(pks) == 0:
                raise ValueError("server_onupdate argument only available for tables with primary key columns.")

            conditions = [pk == text(f'OLD.{pk.name}') for pk in pks]
            condition = functools.reduce(lambda x, y: x & y, conditions)

            trigger = Trigger(
                timing='after',
                event='update',
                on=table,
                action=update(table).where(condition).values({column.name: column.server_onupdate.arg}),
                name=f'{column.name}_server_onupdate',
            )
            
            triggers.append(trigger)
            
    return triggers

@lib.clstools.attr_repr
@lib.clstools.attr_str
class Trigger:
    allowed_timings = ('before', 'after', 'instead_of')
    allowed_events = ('delete', 'insert', 'update')
    allowed_on_types = (FromClause, ColumnElement, ColumnCollection)
    
    def __init__(self, timing, event, on, action, when=None, name=None):
        if timing not in Trigger.allowed_timings:
            raise ValueError(f"timing must be one of {Trigger.allowed_timings}, but {timing=}.")
            
        if event not in Trigger.allowed_events:
            raise ValueError(f"event must be one of {Trigger.allowed_events}, but {event=}.")
            
        if not isinstance(on, Trigger.allowed_on_types):
            raise TypeError(f"on must be one of {Trigger.allowed_on_types}, but {type(on)=}.")
            
        if name is None:
            name = f"trigger_{str(uuid.uuid4()).replace('-', '_')}"
            
        self.timing = timing
        self.event = event
        self.on = on
        self.action = action
        self.when = when
        self.name = name
        
    @classmethod
    def from_sql(cls, db, sql):
        literal_pattern = """([^'"]|"[^"]*"|'[^']*')"""
        pattern = (
            f"CREATE (TEMP |TEMPORARY )?TRIGGER (IF NOT EXISTS )?(.*?\.)?(?P<name>{literal_pattern}*) "
            "(?P<timing>BEFORE|AFTER|INSTEAD OF) (?P<event>DELETE|INSERT|UPDATE) "
            f"(OF (?P<columns>{literal_pattern}*) )?ON (?P<table_name>{literal_pattern}*) "
            f"(FOR EACH ROW )?(WHEN (?P<when>{literal_pattern}*) )?"
            f"BEGIN (?P<action>{literal_pattern}*); END"
        )
        match = re.match(pattern, sql, re.IGNORECASE)

        attrs = {k: match.group(k) for k in ['name', 'timing', 'event', 'columns', 'table_name', 'when', 'action']}
        attrs['name'] = attrs['name'].strip("'").strip('"')
        attrs['timing'] = attrs['timing'].lower()
        attrs['event'] = attrs['event'].lower()
        attrs['table_name'] = attrs['table_name'].strip("'").strip('"')
        if attrs['columns'] is not None:
            pattern = f"({attrs['table_name']}\.)?(?P<column>{literal_pattern}*)"
            columns = [re.match(pattern, column.strip(' ')).group('column').strip("'").strip('"') for column in attrs['columns'].split(',')]
            attrs['on'] = db[attrs['table_name']].table.c[tuple(columns)]
        else:
            attrs['on'] = db[attrs['table_name']].table
        attrs['action'] = text(attrs['action'])
        
        del attrs['table_name'], attrs['columns']
        
        return cls(**attrs)
    
class CreateTrigger(DDLElement):
    inherit_cache = False
    
    def __init__(self, trigger, if_not_exists=False):
        self.trigger = trigger
        self.if_not_exists = if_not_exists
        
class DropTrigger(DDLElement):
    inherit_cache = False
    
    def __init__(self, trigger, if_exists=False):
        self.trigger = trigger
        self.if_exists = if_exists

@compiles(CreateTrigger)
def compile_create_trigger(element, ddlcompiler, **kw):
    kw['literal_binds'] = True
    sql_compiler = ddlcompiler.sql_compiler
    
    trigger = element.trigger
    if_not_exists = "IF NOT EXISTS" if element.if_not_exists else None
    
    timing = trigger.timing.upper().replace('_', ' ')
    event = trigger.event.upper()
    on = trigger.on
    action = trigger.action
    when = trigger.when
    name = trigger.name
    
    if isinstance(on, FromClause):
        on = f'ON {sql_compiler.process(on, asfrom=True, **kw)}'
    elif isinstance(on, ColumnElement):
        column = sql_compiler.process(on, **kw)
        table = sql_compiler.process(on.table, asfrom=True, **kw)
        on = f'OF {column} ON {table}'
    else:
        columns = on
        table = columns[0].table
        if not all(column.table == table for column in columns):
            raise ValueError(f"all columns must belong to the same table, but {columns=}.")
            
        columns = ', '.join(sql_compiler.process(column, **kw) for column in columns)
        table = sql_compiler.process(table, asfrom=True, **kw)
        on = f'OF {columns} ON {table}'
        
    action = sql_compiler.process(action, **kw)
    name = sql_compiler.process(literal(name), **kw)
    if when is not None:
        when = f'WHEN {sql_compiler.process(when, **kw)}'
    
    return ' '.join(filter(None, ['CREATE TRIGGER', name, if_not_exists, timing, event, on, when, f'BEGIN {action}; END']))

@compiles(DropTrigger)
def compile_drop_trigger(element, ddlcompiler, **kw):
    kw['literal_binds'] = True
    sql_compiler = ddlcompiler.sql_compiler
    
    if isinstance(element.trigger, str):
        name = element.trigger
    else:
        name = element.trigger.name
    if_exists = 'IF EXISTS' if element.if_exists else None
    
    name = sql_compiler.process(literal(name), **kw)
    
    return ' '.join(filter(None, ['DROP TRIGGER', if_exists, name]))
