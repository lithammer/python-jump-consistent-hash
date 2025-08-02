Jump Consistent Hash
--------------------

.. image:: https://github.com/lithammer/python-jump-consistent-hash/workflows/Python/badge.svg
   :alt: Build Status
   :target: https://github.com/lithammer/python-jump-consistent-hash/actions

Python and C implementation of the jump consistent hash algorithm by John
Lamping and Eric Veach[1]. Tested on Python 3.9+.

Install
-------

To install Jump Consistent Hash, simply run this simple command in your
terminal of choice::

   $ pip install jump-consistent-hash

The C implementation is optional but is about 10x faster than the pure Python
implementation in CPython.

Usage
`````

.. code:: python

   >>> import jump
   >>> jump.hash(256, 1024)
   520

If you want to use a ``str`` as a key instead of an ``int``, you can pass it
through a hash function to compute a real key. Here's a couple of examples
using Python 3:

.. code:: python

   >>> import hashlib
   >>> int(hashlib.md5(b"127.0.0.1").hexdigest(), 16)
   325870950296970981340734819828239218902

   >>> int(hashlib.sha1(b"127.0.0.1").hexdigest(), 16)
   431133456357828263809343936597625557575256328153

   >>> import binascii
   >>> binascii.crc32(b"127.0.0.1") & 0xffffffff
   3619153832

   >>> abs(hash("127.0.0.1"))
   7536019783825143230

Links
`````

[1] http://arxiv.org/pdf/1406.2294v1.pdf
