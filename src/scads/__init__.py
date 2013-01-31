#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from uuid import uuid1
from scads.lru import LRUCache
lrucache = LRUCache(1000)  # XXX: Make configurable / maybe not a module global


class List(object):
    """ The List Data Structure allows to append a infinite number of items
    to the list. The list can then be iterated over.

    Example::
      >>> from scads.ds import DS
      >>> l = List('test', store=DS(), use_cache=False)
      >>> l.append(1)
      >>> l.append(2)
      >>> list(l)
      [1, 2]

    You can (and should!) iter too::
      >>> i = iter(l)
      >>> i.next()
      1
      >>> i.next()
      2
    """
    def __init__(self, name, store, use_cache=True):
        """ Params:

        name: The name of the list - makes it unique in the datastore
        store: a Instance of DS or a compatible datastore
        use_cache: Should we cache the current list-line (HIGHLY RECOMMENDED!)
        """
        self.name = name
        self.store = store

        self._lruname = "List:" + self.name

        self._nextkey = lrucache.get(self._lruname) if use_cache else None
        if self._nextkey is None:
            # create a root
            self._nextkey = self._key("root")
            self._store(value=None, indexes=[self._root_index()])
            lrucache.set(self._lruname, self._nextkey)

    def _key(self, type_="node"):
        """ Create a unique database key for the given type_

        Params:
            type_: either "root" or "node".
        """
        return 'List:%s:%s:%s' % (type_, self.name, uuid1())

    def _root_index(self):
        return 'List:%s' % self.name

    def _store(self, value, indexes=None):
        key = self._nextkey
        self._nextkey = self._key()
        data = {
            'value': value,
            'nextkey': self._nextkey
        }
        self.store.store(key, data, indexes)
        lrucache.set(self._lruname, self._nextkey)

    def append(self, value):
        self._store(value)

    def _get_roots(self):
        return self.store.get_index(self._root_index())

    def __iter__(self):
        for nextkey in self._get_roots():
            item = self.store.get(nextkey)
            nextkey = item['nextkey']  # root's next
            while True:
                item = self.store.get(nextkey)
                if item is None:
                    break
                nextkey = item['nextkey']
                yield item['value']
