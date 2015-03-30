# -*- coding: utf-8 -*-
"""
Jump Consistent Hash
--------------------

Python (3) implementation of the jump consistent hash algorithm by John Lamping
and Eric Veach[1].

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

Links
`````

[1] http://arxiv.org/pdf/1406.2294v1.pdf

"""
from __future__ import print_function

import sys

from setuptools import setup, find_packages, Extension


if sys.version_info < (3, 2):
    print('ERROR: jump-consistent-hash requires Python version 3.2 or newer.',
          file=sys.stderr)
    sys.exit(1)


setup(name='jump_consistent_hash',
      version='1.1.1',
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
          ])
      ],
      test_suite='jump.tests',
      keywords=[
          'jump hash',
          'jumphash',
          'jump consistent hash',
          'consistent hash',
          'hash algorithm',
          'hash'
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'
      ])
