import hashlib
import random

import pytest

import jump

# `jump.c_hash` is None on installs without the optional C extension.
requires_extension = pytest.mark.skipif(
    jump.c_hash is None, reason="C extension is not installed"
)

# `hash` is included because it is the only name in `__all__`, and so the
# only one users are expected to call.
IMPLEMENTATIONS = [
    pytest.param(jump.py_hash, id="py_hash"),
    pytest.param(jump.c_hash, id="c_hash", marks=requires_extension),
    pytest.param(jump.hash, id="hash"),
]

KNOWN_BUCKETS = [
    (1, 1, 0),
    (42, 57, 43),
    (0xDEAD10CC, 1, 0),
    (0xDEAD10CC, 666, 361),
    (256, 1024, 520),
    # 160-bit key, exercising the reduction to 64 bits.
    (int(hashlib.sha1(b"abc").hexdigest(), 16), 5, 2),
    # Negative keys are reinterpreted as unsigned.
    (-42, 57, 8),
]


@pytest.mark.parametrize("jump_hash", IMPLEMENTATIONS)
@pytest.mark.parametrize(("key", "num_buckets", "expected"), KNOWN_BUCKETS)
def test_hash(jump_hash, key, num_buckets, expected):
    assert jump_hash(key, num_buckets) == expected


@pytest.mark.parametrize("jump_hash", IMPLEMENTATIONS)
@pytest.mark.parametrize("num_buckets", [0, -10, -666])
def test_non_positive_bucket_number(jump_hash, num_buckets):
    with pytest.raises(ValueError):
        jump_hash(0xDEAD10CC, num_buckets)


@pytest.mark.parametrize("jump_hash", IMPLEMENTATIONS)
@pytest.mark.parametrize("num_buckets", [2**31, -(2**31) - 1])
def test_bucket_number_outside_int32(jump_hash, num_buckets):
    with pytest.raises(OverflowError):
        jump_hash(0xDEAD10CC, num_buckets)


@pytest.mark.parametrize("jump_hash", IMPLEMENTATIONS)
@pytest.mark.parametrize(("key", "num_buckets"), [(42, 57.9), (1.5, 57)])
def test_non_integer_argument(jump_hash, key, num_buckets):
    with pytest.raises(TypeError):
        jump_hash(key, num_buckets)


def test_hash_prefers_the_extension():
    """`hash` must be the fast path whenever the extension is installed."""
    expected = jump.py_hash if jump.c_hash is None else jump.c_hash
    assert jump.hash is expected


@requires_extension
def test_implementations_agree():
    """The extension is a drop-in replacement, so it must never diverge."""
    assert jump.c_hash is not None

    rng = random.Random(0xDEAD10CC)
    for _ in range(2000):
        key = rng.getrandbits(rng.choice([8, 64, 160]))
        if rng.random() < 0.25:
            key = -key
        num_buckets = rng.randint(1, 2**31 - 1)
        assert jump.py_hash(key, num_buckets) == jump.c_hash(key, num_buckets)
