from collections.abc import Callable

def hash(key: int, num_buckets: int) -> int: ...
def py_hash(key: int, num_buckets: int) -> int: ...

# None on installs without the optional C extension.
c_hash: Callable[[int, int], int] | None
