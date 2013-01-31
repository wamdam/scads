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


Key features
============

All (write)-access and thus all operations against the database (which may
be eventually consistent) are

 * monotonic: We add data only. No modification of stored data is allowed,
   so we do not need vector-clock support or transaction management stuff.
 * idempotent: All data structures can be fed with data in any order.


