import sys

from _jump import hash as fasthash


__all__ = ['hash', 'fasthash']

if sys.version_info[0] > 2:
    long = int


def hash(key, num_buckets):
    """Generate a number in the range [0, num_buckets).

    Fast, minimal memory, consistent hash algorithm (Jump Consistent Hash).

    Args:
        key (int): The key to hash.
        num_buckets (int): Number of buckets to use.

    Returns:
        The bucket number `key` computes to.

    Raises:
        ValueError: If `num_buckets` is not a positive number.
    """
    b, j = -1, 0

    if num_buckets < 1:
        raise ValueError('num_buckets must be a positive number')

    while j < num_buckets:
        b = int(j)
        key = ((key * long(2862933555777941757)) + 1) & 0xffffffffffffffff
        j = float(b + 1) * (float(1 << 31) / float((key >> 33) + 1))

    return int(b)
