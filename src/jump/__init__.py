"""Fast, minimal memory, consistent hash algorithm."""

try:
    from _jump import hash as c_hash
except ImportError:
    c_hash = None

__all__ = ["hash"]


def py_hash(key, num_buckets):
    """Generate a number in the range [0, num_buckets).

    Args:
        key (int): The key to hash.
        num_buckets (int): Number of buckets to use.

    Returns:
        The bucket number `key` computes to.

    Raises:
        ValueError: If `num_buckets` is not a positive number.
    """
    b, j = -1, 0.0

    if num_buckets < 1:
        raise ValueError(
            f"'num_buckets' must be a positive number, got {num_buckets}"
        )

    while j < num_buckets:
        b = int(j)
        key = ((key * int(2862933555777941757)) + 1) & 0xFFFFFFFFFFFFFFFF
        j = float(b + 1) * (float(1 << 31) / float((key >> 33) + 1))

    return int(b)


hash = c_hash or py_hash
