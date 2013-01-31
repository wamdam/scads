#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scads.lru import LRUCache
from timeit import timeit


def test_cache_set_get():
    cache = LRUCache(5)
    assert cache.get('key') is None
    cache.set('key', 'value')
    assert cache.get('key') == 'value'


def test_cache_set_get_unicode():
    cache = LRUCache(5)
    assert cache.get(u'ä') is None
    cache.set(u'ä', u'ö')
    assert cache.get(u'ä') == u'ö'


def test_cache_set_get_binary():
    cache = LRUCache(5)
    assert cache.get('\xe4\xf6\xfc') is None
    cache.set('\xe4\xf6\xfc', '\xe4\xf6\xfc')
    assert cache.get('\xe4\xf6\xfc') == '\xe4\xf6\xfc'


def test_cache_set_get_two():
    cache = LRUCache(5)
    cache.set('key', 'value')
    cache.set('key2', 'value2')


def test_cache_set_get_full():
    cache = LRUCache(5)
    for i in range(1, 6):
        cache.set(i, i)
    for i in range(1, 6):
        assert cache.get(i) == i


def test_cache_clear():
    cache = LRUCache(1)
    cache.set(1, 1)
    cache.clear()
    assert len(cache.db) == 0
    assert cache.get(1) is None


def test_cache_forget():
    cache = LRUCache(5)
    for i in range(1, 7):
        cache.set(i, i)

    # forgot 1, because it was the oldest
    assert cache.get(1) is None

    for i in range(2, 7):
        assert cache.get(i) == i


def test_cache_forget_lru_get():
    cache = LRUCache(5)
    for i in range(1, 6):
        cache.set(i, i)

    # access all but 5
    for i in range(1, 5):
        cache.get(i)

    # add one
    cache.set(6, 6)

    # and expect 5 to be gone
    assert cache.get(5) is None


def test_cache_forget_lru_set_again():
    cache = LRUCache(5)
    # make the cache full
    for i in range(1, 6):
        cache.set(i, i)

    # access all but 5
    for i in range(1, 5):
        cache.set(i, i)

    # add one
    cache.set(6, 6)

    # and expect 5 to be gone
    assert cache.get(5) is None


def test_cache_forget_many():
    cache = LRUCache(5)
    for i in xrange(1, 1000):
        cache.set(i, i)

    assert len(cache.db) == 5
    for i in range(995, 1000):
        assert cache.get(i) == i


def test_cache_performance_set():
    r = timeit(
        setup="from random import random;"
              "from scads.lru import LRUCache;"
              "cache=LRUCache(10000);",
        stmt="r = random(); cache.set(r, r)",
        number=10000
    )
    assert r < 0.1


def test_cache_performance_get():
    r = timeit(
        setup="from random import randint;"
              "from scads.lru import LRUCache;"
              "cache=LRUCache(10000);"
              "[cache.set(i, True) for i in xrange(10000)]",
        stmt="r = randint(0, 9999); cache.get(r)",
        number=10000
    )
    assert r < 0.1


def test_cache_linear_performance():
    # test more sets and gets
    r1 = timeit(
        setup="from random import randint;"
              "from scads.lru import LRUCache;"
              "cache=LRUCache(10000);",
        stmt="r = randint(0, 9999); cache.set(r+1, True); cache.get(r)",
        number=1000
    )

    r2 = timeit(
        setup="from random import randint;"
              "from scads.lru import LRUCache;"
              "cache=LRUCache(10000);",
        stmt="r = randint(0, 9999); cache.set(r+1, True); cache.get(r)",
        number=10000
    )

    assert r2 * 0.8 <= r1 * 10 <= r2 * 1.2

    # test bigger cache (shouldn't impact performance, just ram)
    r1 = timeit(
        setup="from random import randint;"
              "from scads.lru import LRUCache;"
              "cache=LRUCache(1000);",
        stmt="r = randint(0, 9999); cache.set(r+1, True); cache.get(r)",
        number=1000
    )

    r2 = timeit(
        setup="from random import randint;"
              "from scads.lru import LRUCache;"
              "cache=LRUCache(10000);",
        stmt="r = randint(0, 9999); cache.set(r+1, True); cache.get(r)",
        number=1000
    )

    assert r2 * 0.8 <= r1 <= r2 * 1.2
