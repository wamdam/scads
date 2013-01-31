.. Scalable Data Structures documentation master file, created by
   sphinx-quickstart on Thu Jan 31 21:28:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================================
Welcome to Scalable Data Structures's documentation!
====================================================

**Pragmatic CRDT-like data structures for usage in distributed python
applications with (currently) riak.**

This will be a collection of data primitives like lists, sets, counters and
others, implemented so that a distributed application (i.e. one that runs
either completely or in parts on multiple nodes) can work with them reliably
on a eventually consistent datastore.

Currently, there's only a riak integration. However it'll take about 20 LOC to
support cassandra or others.


.. toctree::
   :maxdepth: 2

   api.rst


Key features
============

All (write)-access and thus all operations against the database (which may
be eventually consistent) are

 * monotonic: We add data only. No modification of stored data is allowed,
   so we do not need vector-clock support or transaction management stuff.
 * idempotent: All data structures can be fed with data in any order.


Exchangable Data-Stores
=======================

A Data-Store ("DS") is responsible for persisting data into some sort of
storage. This storage may be consistent or eventually consistent.

A Data-Store currently requires only these functions to be implemented.

**store(key, value, indexes)**

Store a value under a key and add the key to the indexes named in the list
``indexes``.

**get_index(index)**

Get a list of keys from an index called ``index``.

**get(key)**

Get the value for a given ``key``

**clear()**

Mostly required for tests right now. Clears the datastore.

.. note::

    Be aware that especially deleting methods like ``clear()`` work with some
    delay in a eventually consistent database.


Data Types
==========

List
----

This is a unordered append-only list of items. Key-features:

 * Iterate over a unlimited list with no memory impact
 * O(1) access for each iteration

Usage::

  >>> from scads.ds import DS
  >>> from scads import List
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

.. note::

    We're using ``use_cache=False`` here in order to avoid to append to a
    already existing list from other tests or doctests. In production use,
    you should leave this option to its default.

.. TODO::

   * Evaulate item deletion (prev.next = next, del, ...)
   * set use_cache=False as default in test-cases


Set
---

TBD


Counter
-------

TBD





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
=======

.. toctree::
   :maxdepth: 1

   GPLv3.rst
