from datetime import datetime
import contextlib

import pytest
import sqlalchemy as sa
import pandas as pd
import numpy as np
import hyclib as lib

import dfdb
from dfdb.dataframe import (
    Column,
    Row,
    Item,
)

@pytest.fixture
def db():
    return dfdb.Database(drivername='sqlite') # in-memory SQLite database

@pytest.fixture
def df0():
    df = pd.DataFrame({
        'a': [1,2,3,2],
        'b': [5,6,7,8],
        'c': ['a','b','d','c'],
        'd': [1,2,4,3],
    })
    return df

@pytest.fixture
def df1a():
    df = pd.DataFrame({
        'a': [1,3,3,4],
        'b': [5,7,7,6],
        'c': ['e','f','g','h'],
        'd': [1,2,3,4],
    })
    return df

@pytest.fixture
def df1b():
    df = pd.DataFrame({
        'a': [5,7,7,6],
        'b': [1,3,3,4],
        'e': ['e','f','g','h'],
        'f': [1,2,3,4],
    })
    return df

@pytest.fixture
def df_mixed():
    df = pd.DataFrame({
        'int16': [1,2,3,4],
        'int32': [2,1,4,3],
        'int64': [3,4,2,1],
        'Int16_': [4,3,2,pd.NA],
        'Int32_': [3,pd.NA,1,4],
        'Int64_': [pd.NA,1,3,4],
        'float32': [1.0,2.0,3.0,np.nan],
        'float64': [2.5,1.5,np.nan,-2.3],
        'bool': [True, False, True, False],
        'boolean': [False, True, True, pd.NA],
        'str1': ['dog','123hi','doggo','foobar'],
        'str2': ['og', '12', 'gg', 'fbar'],
        'category': ['hi', 'bye', 'hi', 'bye'],
        'json': [{'a': 1, 'b': {'c': [2, 3]}}, {'a': 3, 'b': {'c': [4]}}, {'c': 1, 'b': {'d': 5}}, {'c': 2}],
        'numpy': [np.array([1, 2, 3]), np.array([[2.0, np.nan]]), np.array([1.0 + 1.0j, 2.0 + 2.0j]), np.array(3.0j)],
        'time': [datetime(2023,1,1), datetime(2023,1,2,3), datetime(2023,1,3), datetime(2023,1,4)],
    })
    df = df.astype({k: k.strip('_') for k in df.columns if k not in ['str1', 'str2', 'json', 'numpy', 'time']})
    return df

def rand_string(length, size=None, chars=None, varlength=True):
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz'
    chars = np.array(list(chars))

    if size is None:
        size = (1,)
    elif isinstance(size, int):
        size = (size,)
    
    if not isinstance(size, tuple):
        raise TypeError(f"size must be a tuple, but {type(size)=}.")
    
    shape = (*size, length)
    s = chars[np.random.randint(len(chars), size=shape)].reshape(-1, length)
    mask = np.random.randint(2, size=s.shape, dtype=bool)
    mask[:,0] = True
    s = np.array([''.join(si[maski]) for si, maski in zip(s, mask)]).reshape(size)
    return s.squeeze()

@pytest.fixture
def df0_long(request):
    M, N, L, chars, O = request.param
    keys = ['a', 'b', 'c', 'd']
    seeds = [0, 1, 2, 3]
    
    df = {}
    for k, seed in zip(keys, seeds):
        with lib.random.set_seed(seed):
            na_indices = np.random.choice(N, size=O, replace=False)
            
            if k == 'a':
                data = np.random.normal(size=N)
            elif k == 'b':
                data = rand_string(L, size=N, chars=chars)
            elif k == 'c':
                data = np.random.randint(M, size=N).astype(float)
            elif k == 'd':
                data = np.random.randint(M, size=N).astype(float)
                
        data[na_indices] = np.nan
        df[k] = data
    
    return pd.DataFrame(df)

@pytest.fixture
def df1_long(request):
    M, N, L, chars, O = request.param
    keys = ['e', 'f', 'c', 'd']
    seeds = [4, 5, 6, 7]
    
    df = {}
    for k, seed in zip(keys, seeds):
        with lib.random.set_seed(seed):
            na_indices = np.random.choice(N, size=O, replace=False)
            
            if k == 'e':
                data = np.random.normal(size=N)
            elif k == 'f':
                data = rand_string(L, size=N, chars=chars)
            elif k == 'c':
                data = np.random.randint(M, size=N).astype(float)
            elif k == 'd':
                data = np.random.randint(M, size=N).astype(float)
                
        data[na_indices] = np.nan
        df[k] = data
    
    return pd.DataFrame(df)
    

@pytest.mark.parametrize(
    'with_schema',
    [True, False],
)
def test_save_load(tmp_path, df_mixed, with_schema):
    drivername, database = 'sqlite', str(tmp_path / 'database.db')
    
    db = dfdb.Database(drivername=drivername, database=database)
    if with_schema:
        _df_mixed = df_mixed.astype({'category': 'object'})
        columns = (sa.Column(k, dfdb.infer_sqlalchemy_type(v) if k != 'json' else sa.JSON) for k, v in _df_mixed.items())
        db['df_mixed'] = dfdb.TableDef(*columns)
        db['df_mixed'].append(_df_mixed)
    else:
        db['df_mixed'] = df_mixed
    
    db = dfdb.Database(drivername=drivername, database=database)
    
    pd.testing.assert_frame_equal(df_mixed, db['df_mixed'].fetch().astype({'category': 'category'}))
    

@pytest.mark.parametrize(
    'ldf, rdf, on, left_on, right_on, suffixes',
    [
        ('df0', 'df1a', None, None, None, ('_x', '_y')),
        ('df0', 'df1a', ('a', 'b'), None, None, ('_0', '_1')),
        ('df0', 'df1a', None, ('a', 'b'), ('a', 'b'), ('_x', '_y')),
        ('df0', 'df1b', None, None, None, ('_x', '_y')),
        ('df0', 'df1b', None, ('a', 'b'), ('b', 'a'), ('_x', '_y')),
    ],
)
@pytest.mark.parametrize(
    'how',
    [
        'inner',
        'left',
        'right',
        'outer',
    ],
)
@pytest.mark.parametrize(
    'sort',
    [True, False],
)
@pytest.mark.parametrize(
    'indicator',
    [True, False],
)
def test_merge(request, db, ldf, rdf, on, left_on, right_on, suffixes, how, sort, indicator):
    ldf, rdf = request.getfixturevalue(ldf), request.getfixturevalue(rdf)
    
    db['ldf'] = ldf
    db['rdf'] = rdf
    
    sqldf = db['ldf'].merge(db['rdf'], how=how, on=on, left_on=left_on, right_on=right_on, sort=sort, suffixes=suffixes, indicator=indicator).fetch(nullable_policy=False) # pandas converts int to float intsead of using Int when there are new NA values due to merging
    
    if indicator:
        sqldf = sqldf.astype({'_merge': pd.CategoricalDtype(['left_only', 'right_only', 'both'])})
        
    df = ldf.merge(rdf, how=how, on=on, left_on=left_on, right_on=right_on, sort=sort, suffixes=suffixes, indicator=indicator)

    pd.testing.assert_frame_equal(df, sqldf)
    
    
@pytest.mark.parametrize(
    'ldf, rdf, suffixes',
    [
        ('df0', 'df1a', ('_x', '_y')),
        ('df0', 'df1b', ('_0', '_1')),
    ],
)
@pytest.mark.parametrize(
    'sort',
    [True, False],
)
@pytest.mark.parametrize(
    'indicator',
    [True, False],
)
def test_merge_cross(request, db, ldf, rdf, suffixes, sort, indicator):
    ldf, rdf = request.getfixturevalue(ldf), request.getfixturevalue(rdf)
    
    how = 'cross'
    
    db['ldf'] = ldf
    db['rdf'] = rdf
    
    sqldf = db['ldf'].merge(db['rdf'], how=how, sort=sort, suffixes=suffixes, indicator=indicator).fetch()
    
    if indicator:
        sqldf = sqldf.astype({'_merge': pd.CategoricalDtype(['left_only', 'right_only', 'both'])})
        
    df = ldf.merge(rdf, how=how, sort=sort, suffixes=suffixes, indicator=indicator)
    
    pd.testing.assert_frame_equal(df, sqldf)
    
    
@pytest.mark.parametrize(
    'df0_long, df1_long',
    [
        ((2, 20, 3, 'ab', 5), (2, 20, 3, 'ab', 5)),
    ],
    indirect=True
)
@pytest.mark.parametrize(
    'how',
    ['inner', 'left', 'right', 'outer', 'cross'],
)
@pytest.mark.parametrize(
    'sort',
    [True, False],
)
@pytest.mark.parametrize(
    'indicator',
    [True, False],
)
def test_merge_long(request, db, df0_long, df1_long, how, sort, indicator):
    ldf, rdf = df0_long, df1_long
    
    db['ldf'] = ldf
    db['rdf'] = rdf
    
    sqldf = db['ldf'].merge(db['rdf'], how=how, sort=sort, indicator=indicator).fetch()
    
    if indicator:
        sqldf = sqldf.astype({'_merge': pd.CategoricalDtype(['left_only', 'right_only', 'both'])})
        
    df = ldf.merge(rdf, how=how, sort=sort, indicator=indicator)
    
    if not sort:
        df = df.sort_values(by=df.columns.tolist(), ignore_index=True)
        sqldf = sqldf.sort_values(by=sqldf.columns.tolist(), ignore_index=True)
        
    pd.testing.assert_frame_equal(df, sqldf)
    
@pytest.mark.parametrize(
    'method',
    ['dataframe', 'series', 'list_tuple', 'list_dict', 'dict', 'tuple'],
)
@pytest.mark.parametrize(
    'omit',
    [False, True],
)
def test_append(db, df_mixed, method, omit):
    df = df_mixed.iloc[:2]
    db['df'] = df
    
    appended_df = df_mixed.iloc[2:]
    
    if omit:
        cols = ['Int16_', 'boolean']
        appended_df = appended_df.drop(columns=cols)
    
    if method not in ['list_tuple', 'tuple']:
        perm = np.random.permutation(len(appended_df.columns))
        appended_df = appended_df.reindex(columns=appended_df.columns[perm])

    if method == 'dataframe':
        db['df'].append(appended_df)
    elif method == 'series':
        for _, row in appended_df.iterrows():
            db['df'].append(row)
    elif method == 'list_tuple':
        rows = [tuple(row.values()) for row in appended_df.to_dict('records')]
        with pytest.raises(sa.exc.StatementError) if omit else contextlib.nullcontext():
            db['df'].append(rows)
    elif method == 'list_dict':
        db['df'].append(appended_df.to_dict('records'))
    elif method == 'dict':
        for _, row in appended_df.iterrows():
            db['df'].append(row.to_dict())
    elif method == 'tuple':
        with pytest.raises(sa.exc.StatementError) if omit else contextlib.nullcontext():
            for row in appended_df.to_dict('records'):
                db['df'].append(tuple(row.values()))
    
    expected = df_mixed.copy()
    if omit:
        expected.loc[2:, cols] = pd.NA
        
    with pytest.raises(Exception) if omit and method in ['list_tuple', 'tuple'] else contextlib.nullcontext():
        pd.testing.assert_frame_equal(expected, db['df'].fetch().astype({'category': 'category'}))
        
@pytest.mark.parametrize(
    'col_idx',
    [
        'int16',
        ['int16', 'float32', 'bool'],
        slice(None),
        Ellipsis,
    ],
)
@pytest.mark.parametrize(
    'row_idx',
    [
        None,
        0,
        2,
        slice(None),
        slice(None, 2),
        slice(1,3),
        Ellipsis,
    ],
)
def test_getitem(db, df_mixed, col_idx, row_idx):
    # drop columns that use ExtensionDtype since our inference of dtype
    # depends on whether the column consists of None or not, meaning
    # that if we selected rows that do not include None then the dtype will be different.
    df = df_mixed.drop(columns=['Int16_', 'Int32_', 'Int64_', 'boolean'])
    
    db['df'] = df
    if col_idx is not None and row_idx is not None:
        output = db['df'][col_idx, row_idx]
        if col_idx is Ellipsis:
            col_idx = slice(None)
        expected = df[col_idx].iloc[row_idx]
    elif col_idx is not None:
        output = db['df'][col_idx]
        if col_idx is Ellipsis:
            col_idx = slice(None)
        expected = df[col_idx]
    else:
        raise RuntimeError("Shouldn't end up here.")
        
    if isinstance(expected, pd.DataFrame):
        expected = expected.reset_index(drop=True)
        output = output.fetch()
        if 'category' in output:
            output = output.astype({'category': 'category'})
        pd.testing.assert_frame_equal(expected, output)
        
    elif isinstance(expected, pd.Series):
        check_names = True
        if isinstance(output, Column):
            expected = expected.reset_index(drop=True) # Column index is always just the default range index
        elif isinstance(output, Row):
            check_names = False # Row name comes from the Column index, so name may not match
        else:
            raise RuntimeError("Shouldn't end up here.")
            
        output = output.fetch()
        if output.name == 'category':
            output = output.astype('category')
        pd.testing.assert_series_equal(expected, output, check_names=check_names)
        
    else:
        output = output.fetch()
        assert expected == output
    
@pytest.mark.parametrize(
    'col_idx',
    [
        None,
        'int16',
        ['int16', 'float32', 'bool'],
        slice(None),
        Ellipsis,
    ],
)
@pytest.mark.parametrize(
    'row_idx',
    [
        0,
        2,
        slice(None),
        slice(None, 2),
        slice(1,3),
        Ellipsis,
    ],
)
def test_loc_getitem(db, df_mixed, row_idx, col_idx):
    # drop columns that use ExtensionDtype since our inference of dtype
    # depends on whether the column consists of None or not, meaning
    # that if we selected rows that do not include None then the dtype will be different.
    df = df_mixed.drop(columns=['Int16_', 'Int32_', 'Int64_', 'boolean'])
    
    db['df'] = df
    if col_idx is not None and row_idx is not None:
        output = db['df'].loc[row_idx, col_idx]
        if col_idx is Ellipsis:
            col_idx = slice(None)
        expected = df.loc[row_idx, col_idx]
    elif row_idx is not None:
        output = db['df'].loc[row_idx]
        if row_idx is Ellipsis:
            row_idx = slice(None)
        expected = df.loc[row_idx]
    else:
        raise RuntimeError("Shouldn't end up here.")
        
    if isinstance(expected, pd.DataFrame):
        expected = expected.reset_index(drop=True)
        output = output.fetch()
        if 'category' in output:
            output = output.astype({'category': 'category'})
        pd.testing.assert_frame_equal(expected, output)
        
    elif isinstance(expected, pd.Series):
        check_names = True
        if isinstance(output, Column):
            expected = expected.reset_index(drop=True) # Column index is always just the default range index
        elif isinstance(output, Row):
            check_names = False # Row name comes from the Column index, so name may not match
        else:
            raise RuntimeError("Shouldn't end up here.")
            
        output = output.fetch()
        if output.name == 'category':
            output = output.astype('category')
        pd.testing.assert_series_equal(expected, output, check_names=check_names)
        
    else:
        output = output.fetch()
        assert expected == output
        
@pytest.mark.parametrize(
    'row_idx',
    [
        0,
        2,
        slice(None),
        slice(None, 2),
        slice(1,3),
        Ellipsis,
    ],
)
def test_iloc_getitem(db, df_mixed, row_idx):
    # drop columns that use ExtensionDtype since our inference of dtype
    # depends on whether the column consists of None or not, meaning
    # that if we selected rows that do not include None then the dtype will be different.
    df = df_mixed.drop(columns=['Int16_', 'Int32_', 'Int64_', 'boolean'])
    
    db['df'] = df
    
    output = db['df'].iloc[row_idx]
    if row_idx is Ellipsis:
        row_idx = slice(None)
    expected = df.iloc[row_idx]
        
    if isinstance(expected, pd.DataFrame):
        expected = expected.reset_index(drop=True)
        output = output.fetch()
        if 'category' in output:
            output = output.astype({'category': 'category'})
        pd.testing.assert_frame_equal(expected, output)
        
    elif isinstance(expected, pd.Series):
        output = output.fetch()
        if output.name == 'category':
            output = output.astype('category')
        pd.testing.assert_series_equal(expected, output, check_names=False)
        
    else:
        raise RuntimeError("Shouldn't be here.")
        
@pytest.mark.parametrize(
    'df0_long',
    [(2, 20, 3, 'ab', 5)],
    indirect=True,
)
@pytest.mark.parametrize(
    'by',
    [
        'a',
        'b',
        'c',
        ['a','b'],
        ['b','c'],
        ['c','d'],
        ['d','c','b'],
    ]
)
@pytest.mark.parametrize(
    'ascending',
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    'na_position',
    [
        'first',
        'last',
    ],
)
def test_sort_values(db, df0_long, by, ascending, na_position):
    db['df'] = df0_long
    
    output = db['df'].sort_values(by, ascending=ascending, na_position=na_position).fetch()
    expected = df0_long.sort_values(by, ascending=ascending, na_position=na_position, kind='stable').reset_index(drop=True)

    pd.testing.assert_frame_equal(output, expected)
    
def test_to_html_mixed(db, df_mixed):
    db['df'] = df_mixed
    assert db['df'].to_html() == df_mixed.to_html()
    
@pytest.mark.parametrize(
    'df0_long',
    [
        (2, 20, 3, 'ab', 5),
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    'show_dimensions',
    [
        False,
        True,
        'truncate',
    ],
)
@pytest.mark.parametrize(
    'max_rows',
    [
        15,
        None,
    ],
)
def test_to_html_long(db, df0_long, show_dimensions, max_rows):
    db['df'] = df0_long
    output = db['df'].to_html(show_dimensions=show_dimensions, max_rows=max_rows)
    expected = df0_long.to_html(show_dimensions=show_dimensions, max_rows=max_rows)
    assert output == expected

@pytest.mark.parametrize(
    'func, klass, indexable, allowed_dtypes',
    [
        (lambda x: x.isna(), Column, True, None),
        (lambda x: x.isnull(), Column, True, None),
        (lambda x: x.max(), Item, False, None),
        (lambda x: x.min(), Item, False, None),
        (lambda x: x.any(), Item, False, ['bool']),
        (lambda x: x.all(), Item, False, ['bool']),
        (lambda x: x.unique(), Column, False, None),
        (lambda x: x.nunique(), Item, False, None),
        (lambda x: -x, Column, True, ['numeric']),
        (lambda x: +x, Column, True, ['numeric']),
        (lambda x: ~x, Column, True, ['bool']),
    ],
)
@pytest.mark.parametrize(
    'col_name, dtype',
    [
        ('int16', 'numeric'),
        ('Int16_', 'numeric'),
        ('bool', 'bool'),
        ('boolean', 'bool'),
        ('str1', 'str'),
    ],
)
def test_unary_column_ops(db, df_mixed, col_name, dtype, func, klass, indexable, allowed_dtypes):
    db['df'] = df_mixed
    
    valid = allowed_dtypes is None or dtype in allowed_dtypes
    
    with contextlib.nullcontext() if valid else pytest.raises(TypeError):
        col = func(db['df'][col_name])
    
    if not valid:
        return
    
    assert isinstance(col, klass)
    if klass is Column:
        assert col.indexable == indexable
    
    output = col.fetch()
    expected = func(df_mixed[col_name])
    
    if isinstance(expected, pd.Series):
        pd.testing.assert_series_equal(output, expected)
    elif isinstance(expected, (np.ndarray, pd.api.extensions.ExtensionArray)):
        assert (output == expected).all()
    else:
        assert output == expected
        
@pytest.mark.parametrize(
    'func, allowed_dtypes, skip_dtypes, reversible',
    [
        (lambda x, y: x + y, ['int', 'float', 'bool'], None, True),
        (lambda x, y: x - y, ['int', 'float', 'bool'], ['bool'], True), # pandas does not support bool subtraction
        (lambda x, y: x * y, ['int', 'float', 'bool'], None, True),
        (lambda x, y: x / y, ['int', 'float', 'bool'], ['bool'], True), # pandas does not support bool truediv
        (lambda x, y: x // y, ['int', 'float', 'bool'], ['bool'], True),  # pandas does not support bool floordiv
        (lambda x, y: x ** y, ['int', 'float', 'bool'], ['bool'], True), # pandas does not support bool pow
        (lambda x, y: x % y, ['int', 'bool'], ['bool'], True), # skip bool since there appears to be a pandas bug
        (lambda x, y: x & y, ['bool'], None, True),
        (lambda x, y: x | y, ['bool'], None, True),
        (lambda x, y: x ^ y, [], None, True), # sqlite does not currently support xor
        (lambda x, y: x == y, None, ['float', 'list'], True), # sqlite can't distinguish between NaN and NULL
        (lambda x, y: x != y, None, ['float', 'list'], True), # sqlite can't distinguish between NaN and NULL
        (lambda x, y: x < y, None, ['float', 'list'], True), # sqlite can't distinguish between NaN and NULL
        (lambda x, y: x <= y, None, ['float', 'list'], True), # sqlite can't distinguish between NaN and NULL
        (lambda x, y: x > y, None, ['float', 'list'], True), # sqlite can't distinguish between NaN and NULL
        (lambda x, y: x >= y, None, ['float', 'list'], True), # sqlite can't distinguish between NaN and NULL
        (lambda x, y: x.isin(y), None, ['int', 'float', 'bool', 'str'], False),
        (lambda x, y: x.str.contains(y), ['str'], None, False),
        (lambda x, y: x.str.startswith(y), ['str'], None, False),
        (lambda x, y: x.str.endswith(y), ['str'], None, False),
    ],
)
@pytest.mark.parametrize(
    'col_name_1, col_name_2, constants, dtype',
    [
        ('int16', 'Int16_', [7], 'int'),
        ('Int16_', 'Int32_', [7], 'int'),
        ('float32', 'float64', [7.3], 'float'),
        ('bool', 'boolean', [True, False], 'bool'),
        ('boolean', 'bool', [True, False], 'bool'),
        ('str1', None, ['og', 'gg', 'do'], 'str'),
        ('int16', None, [[3,4], (2,3)], 'list'),
    ],
)
def test_binary_column_ops(db, df_mixed, col_name_1, col_name_2, constants, dtype, func, allowed_dtypes, skip_dtypes, reversible):
    if skip_dtypes is not None and dtype in skip_dtypes:
        return
    
    db['df'] = df_mixed
    
    valid = allowed_dtypes is None or dtype in allowed_dtypes
    
    sqlcol1 = db['df'][col_name_1]
    sqlcol2 = db['df'][col_name_2] if col_name_2 is not None else None
    col1 = df_mixed[col_name_1]
    col2 = df_mixed[col_name_2] if col_name_2 is not None else None
    
    sql_args = []
    args = []
    
    for const in constants:
        sql_args.append((sqlcol1, const))
        args.append((col1, const))
        if reversible:
            sql_args.append((const, sqlcol1))
            args.append((const, col1))
        if sqlcol2 is not None:
            sql_args.append((sqlcol1, sqlcol2))
        if col2 is not None:
            args.append((col1, col2))
    
    for (sql_x, sql_y), (x, y) in zip(sql_args, args):
        with contextlib.nullcontext() if valid else pytest.raises(TypeError):
            col = func(sql_x, sql_y)
            
        if not valid:
            continue
            
        expected = func(x, y)

        assert isinstance(col, Column)
        assert col.indexable

        output = col.fetch()
        
        check_dtype = True
        if 'bool' in expected.dtype.name and not expected.isna().any():
            assert output.dtype.name in ['bool', 'boolean']
            check_dtype = False # if expected has no NA and is a bool, either bool or boolean is correct
        elif 'float' in expected.dtype.name.lower():
            assert output.dtype.name.lower() == expected.dtype.name.lower()
            check_dtype = False # allow float dtypes to be either nullable or not, since it doens't matter
        elif expected.dtype.name.lower() == 'int8':
            nullable = expected.dtype.name[0].isupper()
            assert output.dtype.name == 'Int16' if nullable else 'int16'
            check_dtype = False # since sqlalchemy doesn't support int8, int16 is the closest correct dtype
            
        pd.testing.assert_series_equal(output, expected, check_dtype=check_dtype)
           
@pytest.mark.parametrize(
    'col_func, expected, name',
    (
        [lambda df: df['json'].json['a'], [1, 3, None, None], 'json.a'],
        [lambda df: df['json'].json['b'], [{'c': [2, 3]}, {'c': [4]}, {'d': 5}, None], 'json.b'],
        [lambda df: df['json'].json['c'], [None, None, 1, 2], 'json.c'],
        [lambda df: df['json'].json['a']['b'], [None, None, None, None], 'json.a.b'],
        [lambda df: df['json'].json['b']['c'], [[2, 3], [4], None, None], 'json.b.c'],
        [lambda df: df['json'].json['b']['c'][0], [2, 4, None, None], 'json.b.c.0'],
        [lambda df: df['json'].json['b']['c'][1], [3, None, None, None], 'json.b.c.1'],
    )
)
def test_column_json_ops(db, df_mixed, col_func, expected, name):
    _df_mixed = df_mixed.astype({'category': 'object'})
    columns = (sa.Column(k, dfdb.infer_sqlalchemy_type(v) if k != 'json' else sa.JSON) for k, v in _df_mixed.items())
    db['df'] = dfdb.TableDef(*columns)
    db['df'].append(_df_mixed)
    
    output = col_func(db['df']).fetch()
    assert output.name == name and output.dtype == 'object' and all(u == v for u, v in zip(output, expected))
    
def _getitem(obj, keys, default):
    for key in keys:
        try:
            obj = obj[key]
        except (KeyError, TypeError):
            obj = default
    return obj

@pytest.mark.parametrize(
    'stmt, var, pandas_apply, raises',
    (
        ["bool", None, None, None],
        ["boolean", None, None, None],
        ["bool and boolean", None, None, None],
        ["bool or boolean", None, None, None],
        ["bool < boolean", None, None, None],
        ["int16 == 3", None, None, None],
        ["int16.isin([3,4])", None, None, None],
        ["int16.isin(@var)", [1,3], None, None],
        ["Int16_.isna()", None, None, None],
        ["Int32_ == Int64_", None, None, None],
        ["Int32_ < Int64_", None, None, None],
        ["json.json['b']['c'][0] == 4", None, lambda row: _getitem(row['json'], ['b', 'c', 0], None) == 4, None],
        ["json.json['b']['c'] == [2, 3]", None, lambda row: _getitem(row['json'], ['b', 'c'], None) == [2, 3], TypeError],
        ["str1 == 'dog'", None, None, None],
        ["str1.str.contains('dog')", None, None, None],
        ["str1.str.contains(str2)", None, None, TypeError], # does not support str operations between two column, just like pandas
        ["json.json['a'] == 1 and str1 == 'dog'", None, lambda row: _getitem(row['json'], ['a'], None) == 1 and row['str1'] == 'dog', None],
    )
)
def test_query(db, df_mixed, stmt, var, pandas_apply, raises):
    _df_mixed = df_mixed.astype({'category': 'object'})
    columns = (sa.Column(k, dfdb.infer_sqlalchemy_type(v) if k != 'json' else sa.JSON) for k, v in _df_mixed.items())
    db['df'] = dfdb.TableDef(*columns)
    db['df'].append(_df_mixed)
    
    with contextlib.nullcontext() if raises is None else pytest.raises(raises):
        output = db['df'].query(stmt).fetch()
        
    if raises is not None:
        return
    
    if pandas_apply is None:
        expected = df_mixed.query(stmt)
    else:
        expected = df_mixed.loc[df_mixed.apply(pandas_apply, axis=1)]
    expected = expected.reset_index(drop=True).astype({'category': 'object'})

    assert all('bool' in d1.name if 'bool' in d2.name else d1.name.lower() == d2.name.lower() for _, d1, d2 in lib.itertools.dict_zip(output.dtypes, expected.dtypes))
    
    pd.testing.assert_frame_equal(output, expected, check_dtype=False)
