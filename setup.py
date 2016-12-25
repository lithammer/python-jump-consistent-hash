# -*- coding: utf-8 -*-
from __future__ import print_function

import platform
import sys

from distutils.command.build_ext import build_ext
from distutils.errors import (CCompilerError, DistutilsExecError,
                              DistutilsPlatformError)
from setuptools import setup, find_packages, Extension

with open('README.rst') as f:
    __doc__ = f.read()

IS_PYPY = platform.python_implementation().lower() == 'pypy'

if sys.platform == 'win32' and sys.version_info > (2, 6):
    # 2.6's distutils.msvc9compiler can raise an IOError when failing to
    # find the compiler.
    # It can also raise ValueError http://bugs.python.org/issue7511
    ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError,
                  IOError, ValueError)
else:
    ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)


class BuildFailedError(Exception):
    pass


# This class allows C extension building to fail.
class ve_build_ext(build_ext):

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailedError()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailedError()


ext_modules = {
    'ext_modules': [
        Extension('_jump', sources=[
            'jump/jump.cpp',
            'jump/jumpmodule.c'
        ])
    ]
}


def run_setup(with_binary):
    kwargs = ext_modules if with_binary else {}

    setup(name='jump_consistent_hash',
          version='3.0.0',
          description='Implementation of the Jump Consistent Hash algorithm',
          long_description=__doc__,
          author='Peter Renström',
          license='MIT',
          url='https://github.com/renstrom/python-jump-consistent-hash',
          packages=find_packages(),
          cmdclass={'build_ext': ve_build_ext},
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
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
          ],
          **kwargs)


try:
    run_setup(not IS_PYPY)
except BuildFailedError:
    run_setup(False)
    print('*' * 75)
    print('WARNING: The C extension could not be compiled, '
          'speedups are not enabled.')
    print('Plain-Python installation succeeded.')
    print('*' * 75)
