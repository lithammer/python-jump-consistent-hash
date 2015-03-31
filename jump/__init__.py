import sys

from _jump import hash as fasthash


__all__ = ['hash', 'fasthash']

if sys.version_info[0] > 2:
    long = int


def hash(key, num_buckets):
    """Generate a number in the range [0, num_buckets].

    Fast, minimal memory, consistent hash algorithm (Jump Consistent Hash).

    :param int key: The key to use
    :param int num_buckets: Number of buckets to use
    """
    b, j = -1, 0

    if num_buckets < 1:
        raise ValueError('num_buckets must be greater than 0')

    while j < num_buckets:
        b = int(j)
        key = ((key * long(2862933555777941757)) + 1) & 0xffffffffffffffff
        j = float(b + 1) * (float(1 << 31) / float((key >> 33) + 1))

    return int(b)
