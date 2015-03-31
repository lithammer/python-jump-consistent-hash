# Jump Consistent Hash

[![Build Status](https://travis-ci.org/renstrom/python-jump-consistent-hash.svg?branch=master)](https://travis-ci.org/renstrom/python-jump-consistent-hash)

Python implementation of the jump consistent hash algorithm by John Lamping and Eric Veach[1].

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
