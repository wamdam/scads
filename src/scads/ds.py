#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#from riak import RiakHttpTransport
from collections import defaultdict
from riak import RiakClient
from riak import RiakPbcTransport
import os


class DS(object):
    """ Base class for interacting with a database.
    This implementation stores anything in python / RAM.
    Implement with your database.
    """
    def __init__(self):
        self._db = {}
        self._indexes = defaultdict(list)

    def store(self, key, value, indexes=None):
        self._db[key] = value
        if indexes is not None:
            for index in indexes:
                self._indexes[index].append(key)

    def get_index(self, index):
        return self._indexes[index]

    def get(self, key):
        return self._db.get(key)

    def clear(self):
        """ Wipes all data from this database.
        """
        self._db = {}
        self._indexes = defaultdict(list)


PB_HOST = os.environ.get('RIAK_HOST', 'localhost')
PB_PORT = int(os.environ.get('RIAK_PORT', '8087'))


class DS_Riak(DS):
    """ Riak DS
    """
    def __init__(self, host=PB_HOST, port=PB_PORT, bucketname='_scads'):
        """
        Params:
            host: Hostname or IP Address of the riak database
            port: Port of the riak database
            bucketname: Where to store stuff
        """
        self.client = RiakClient(host, port,
                                 transport_class=RiakPbcTransport,
                                 transport_options={'max_attempts': 3})
        self.bucket = self.client.bucket(bucketname)

    def store(self, key, value, indexes=None):
        obj = self.bucket.get(key)
        obj.set_data(value)
        if indexes is not None:
            for index in indexes:
                obj.add_index('scads_bin', index)
        obj.store()

    def get_index(self, index):
        return self.bucket.get_index('scads_bin', index)

    def get(self, key):
        d = self.bucket.get(key).get_data()
        if d is None:
            return None
        return d

    def clear(self):
        for key in self.bucket.get_keys():
            self.bucket.get(key).delete()


__all__ = ["DS", "DS_Riak"]
