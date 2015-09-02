# Jump Consistent Hash

[![Build Status](https://travis-ci.org/renstrom/python-jump-consistent-hash.svg?branch=master)](https://travis-ci.org/renstrom/python-jump-consistent-hash)

Python implementation of the jump consistent hash algorithm by John Lamping and Eric Veach[1]. Requires Python 2.6-2.7, or 3.2+.

[1] http://arxiv.org/pdf/1406.2294v1.pdf

## Usage

```python
>>> import jump
>>> jump.hash(256, 1024)
520
```

Or if you want to use the C++ extension:

```python
>>> jump.fasthash(256, 1024)
520
```

If you want to use a `str` as a key instead of an `int`, you can pass it through a hash function to compute a real key. Here's a couple of examples using Python 3:

```python
>>> import hashlib
>>> int(hashlib.md5(b'127.0.0.1').hexdigest(), 16)
325870950296970981340734819828239218902

>>> int(hashlib.sha1(b'127.0.0.1').hexdigest(), 16)
431133456357828263809343936597625557575256328153

>>> import binascii
binascii.crc32(b'127.0.0.1')
3619153832

>>> abs(hash('127.0.0.1'))
1745092129592664124
```

## Benchmarks

Here's some benchmarks comparing the pure Python solution vs the C++ extension. Interestingly, the pure Python solution running on PyPy is almost as fast as the C++ variant on CPython. These benchmarks were run on my mid 2013 MacBook Air, so take it with a grain of salt.

**CPython 3.4.3**

```python
>>> timeit.timeit('import jump; jump.hash(256, 1024)', number=1000000)
8.3571082999988
>>> timeit.timeit('import jump; jump.fasthash(256, 1024)', number=1000000)
0.748130168998614
```

**PyPy 3.2.5**

```python
>>>> timeit.timeit('import jump; jump.hash(256, 1024)', number=1000000)
1.1917212009429932
>>>> timeit.timeit('import jump; jump.fasthash(256, 1024)', number=1000000)
4.380352973937988
```

## License

MIT
