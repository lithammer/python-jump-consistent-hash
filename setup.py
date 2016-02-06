# -*- coding: utf-8 -*-
"""
Jump Consistent Hash
--------------------

Python implementation of the jump consistent hash algorithm by John Lamping and
Eric Veach[1]. Requires Python 2.6-2.7 or 3.2+.

Usage
`````

.. code:: python

    >>> import jump
    >>> jump.hash(256, 1024)
    520

Or if you want to use the C++ extension:

.. code:: python

    >>> jump.fasthash(256, 1024)
    520

If you want to use a `str` as a key instead of an `int`, you can pass it
through a hash function to compute a real key. Here's a couple of examples
using Python 3:

.. code:: python

      >>> import hashlib
      >>> int(hashlib.md5(b'127.0.0.1').hexdigest(), 16)
      325870950296970981340734819828239218902

      >>> int(hashlib.sha1(b"127.0.0.1").hexdigest(), 16)
      431133456357828263809343936597625557575256328153

      >>> import binascii
      >>> binascii.crc32(b'127.0.0.1') & 0xffffffff
      3619153832

      >>> abs(hash('127.0.0.1'))
      7536019783825143230

Links
`````

[1] http://arxiv.org/pdf/1406.2294v1.pdf

"""
from setuptools import setup, find_packages, Extension


setup(name='jump_consistent_hash',
      version='2.0.3.globo',
      description='Implementation of the Jump Consistent Hash algorithm',
      long_description=__doc__,
      author='Peter Renström',
      license='MIT',
      url='https://github.com/renstrom/python-jump-consistent-hash',
      packages=find_packages(),
      ext_modules=[
          Extension('_jump', sources=[
              'jump/jump.cpp',
              'jump/jumpmodule.c'
          ], include_dirs=['jump'])
      ],
      data_files=[('_jump', ['jump/jump.h'])],
      test_suite='jump.tests',
      keywords=[
          'jump hash',
          'jumphash',
          'jump consistent hash',
          'consistent hash',
          'hash algorithm',
          'hash'
      ],
      headers=['jump/jump.h'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ])
