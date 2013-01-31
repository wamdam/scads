#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# LRU Cache, based heavily on
# https://code.activestate.com/recipes/
# 578078-py26-and-py30-backport-of-python-33s-lru-cache/

from threading import Lock
lock = Lock()

PREV, NEXT, KEY, VALUE = 0, 1, 2, 3    # names for the link fields


class LRUCache(object):
    def __init__(self, maxsize=100):
        self.maxsize = maxsize
        self.db = {}
        self.root = []
        self.root[:] = [self.root, self.root, None, None]
        self.lock = Lock()

    def _move_link_to_top(self, link):
        link_prev, link_next, key, value = link
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev
        last = self.root[PREV]
        last[NEXT] = self.root[PREV] = link
        link[PREV] = last
        link[NEXT] = self.root

    def set(self, key, value):
        with self.lock:
            link = self.db.get(key)
            if link is not None:
                self._move_link_to_top(link)
                link[VALUE] = value
            elif len(self.db) < self.maxsize:
                # put key in a new link at the front of the list
                last = self.root[PREV]
                link = [last, self.root, key, value]
                self.db[key] = last[NEXT] = self.root[PREV] = link
            else:
                # use root to store the new key and result
                self.root[KEY] = key
                self.root[VALUE] = value
                self.db[key] = self.root
                # empty the oldest link and make it the new root
                self.root = self.root[NEXT]
                del self.db[self.root[KEY]]
                self.root[KEY] = None
                self.root[VALUE] = None

    def get(self, key):
        with self.lock:
            link = self.db.get(key)
            if link is not None:
                self._move_link_to_top(link)
                return link[VALUE]

    def clear(self):
        """Clear the cache and cache statistics"""
        with lock:
            self.db.clear()
            self.root[:] = [self.root, self.root, None, None]
