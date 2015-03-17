from setuptools import setup


setup(name='jump_consistent_hash',
      version='1.0.0',
      description='Implementation of the Jump Consistent Hash algorithm',
      author='Peter Renström',
      license='MIT',
      url='https://github.com/renstrom/python-jump-consistent-hash',
      packages=['jump'],
      test_suite='tests',
      keywords=[
          'jump hash',
          'jumphash',
          'consistent hash',
          'hash algorithm',
          'hash'
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4'
      ])
