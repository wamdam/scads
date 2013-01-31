#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scads import ds
from scads import lrucache
from scads import List
import pytest
import string
import random


def get_stores():
    stores = [getattr(ds, store)() for store in ds.__all__]
    for store in stores:
        store.clear()
    return stores


@pytest.fixture
def listname():
    return "".join([random.choice(string.ascii_lowercase) for x in xrange(12)])


@pytest.mark.parametrize(("store"), get_stores())
def test_list_append(listname, store):
    l = List(listname, store=store, use_cache=False)
    # append 100 items
    for i in xrange(100):
        l.append(i)

    assert len(list(l)) == 100


@pytest.mark.parametrize(("store"), get_stores())
def test_list_iter(listname, store):
    l = List(listname, store=store, use_cache=False)
    for i in xrange(3):
        l.append(i)

    i = iter(l)
    assert next(i) == 0
    assert next(i) == 1
    assert next(i) == 2


@pytest.mark.parametrize(("store"), get_stores())
def test_list_multiroot(listname, store):
    l = List(listname, store=store, use_cache=False)
    for i in xrange(3):
        l.append(i)

    assert(len(l._get_roots()) == 1)
    assert sorted(list(l)) == [0, 1, 2]

    l = List(listname, store=store, use_cache=False)
    for i in xrange(3, 6):
        l.append(i)

    assert(len(l._get_roots()) == 2)
    assert sorted(list(l)) == [0, 1, 2, 3, 4, 5]


@pytest.mark.parametrize(("store"), get_stores())
def test_list_with_cache(listname, store):
    lrucache.clear()  # if we don't clear, it'll find rests of other tests

    l = List(listname, store=store, use_cache=True)
    for i in xrange(3):
        l.append(i)

    assert(len(l._get_roots()) == 1)
    assert sorted(list(l)) == [0, 1, 2]

    l = List(listname, store=store, use_cache=True)
    for i in xrange(3, 6):
        l.append(i)

    assert(len(l._get_roots()) == 1)
    assert sorted(list(l)) == [0, 1, 2, 3, 4, 5]
