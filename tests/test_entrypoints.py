import os.path as osp
import pytest
import warnings

import entrypoints

samples_dir = osp.join(osp.dirname(__file__), 'samples')

sample_path = [
    osp.join(samples_dir, 'packages1'),
    osp.join(samples_dir, 'packages1', 'baz-0.3.egg'),
    osp.join(samples_dir, 'packages2'),
    osp.join(samples_dir, 'packages2', 'qux-0.4.egg'),
]

def test_get_group_all():
    group = entrypoints.get_group_all('entrypoints.test1', sample_path)
    print(group)
    assert len(group) == 5
    assert set(ep.name for ep in group) == {'abc', 'rew', 'opo', 'njn'}

def test_get_group_named():
    group = entrypoints.get_group_named('entrypoints.test1', sample_path)
    print(group)
    assert len(group) == 4
    assert group['abc'].module_name == 'foo'
    assert group['abc'].object_name == 'abc'

def test_get_single():
    ep = entrypoints.get_single('entrypoints.test1', 'abc', sample_path)
    assert ep.module_name == 'foo'
    assert ep.object_name == 'abc'

    ep2 = entrypoints.get_single('entrypoints.test1', 'njn', sample_path)
    assert ep.module_name == 'foo'
    assert ep.object_name == 'abc'

def test_load():
    ep = entrypoints.EntryPoint('get_ep', 'entrypoints', 'get_single', None)
    obj = ep.load()
    assert obj is entrypoints.get_single

def test_bad():
    bad_path = [osp.join(samples_dir, 'packages3')]

    with warnings.catch_warnings(record=True) as w:
        group = entrypoints.get_group_named('entrypoints.test1', bad_path)

    assert 'bad' not in group
    assert len(w) == 1

    with warnings.catch_warnings(record=True) as w2:
        ep = entrypoints.get_single('entrypoints.test1', 'bad')

    assert ep is None
    assert len(w) == 1

def test_parse():
    ep = entrypoints.EntryPoint.from_string(
        'some.module:some.attr [extra1,extra2]', 'foo'
    )
    assert ep.module_name == 'some.module'
    assert ep.object_name == 'some.attr'
    assert ep.extras == ['extra1', 'extra2']

def test_parse_bad():
    with pytest.raises(entrypoints.BadEntryPoint):
        entrypoints.EntryPoint.from_string("this won't work", 'foo')
