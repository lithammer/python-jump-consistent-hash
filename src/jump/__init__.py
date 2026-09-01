"""Fast, minimal memory, consistent hash algorithm."""

import operator

try:
    from _jump import hash as c_hash
except ImportError:
    c_hash = None

__all__ = ["hash"]

_INT32_MIN = -(2**31)
_INT32_MAX = 2**31 - 1


def py_hash(key, num_buckets):
    """Generate a number in the range [0, num_buckets).

    Args:
        key (int): The key to hash.
        num_buckets (int): Number of buckets to use.

    Returns:
        The bucket number `key` computes to.

    Raises:
        TypeError: If `key` or `num_buckets` is not an integer.
        OverflowError: If `num_buckets` is outside the signed 32-bit range.
        ValueError: If `num_buckets` is not a positive number.
    """
    # `hash` is whichever implementation got installed, so these checks must
    # reject exactly what the C extension rejects, in the same order.
    key = operator.index(key)
    num_buckets = operator.index(num_buckets)

    if num_buckets > _INT32_MAX:
        raise OverflowError("signed integer is greater than maximum")
    if num_buckets < _INT32_MIN:
        raise OverflowError("signed integer is less than minimum")
    if num_buckets < 1:
        raise ValueError(
            f"'num_buckets' must be a positive number, got {num_buckets}"
        )

    b, j = -1, 0.0

    while j < num_buckets:
        b = int(j)
        key = (key * 2862933555777941757 + 1) & 0xFFFFFFFFFFFFFFFF
        j = (b + 1) * ((1 << 31) / ((key >> 33) + 1))

    return b


hash = c_hash or py_hash
