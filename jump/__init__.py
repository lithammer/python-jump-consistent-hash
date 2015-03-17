def hash(key: int, num_buckets: int) -> int:
    """Generate a number in the range [0, num_buckets].

    Fast, minimal memory, consistent hash algorithm (Jump Consistent Hash).

    The reference C++ implementation is as follows:

        int32_t JumpConsistentHash(uint64_t key, int32_t num_buckets) {
            int64_t b = -1, j = 0;

            while (j < num_buckets) {
                b = j;
                key = key * 2862933555777941757ULL + 1;
                j = (b + 1) * (double(1LL << 31) / double((key >> 33) + 1));
            }

            return b;
        }

    :param int key: The key to use
    :param int num_buckets: Number of buckets to use
    """
    b, j = -1, 0

    if num_buckets < 0:
        num_buckets = 1

    while j < num_buckets:
        b = int(j)
        key = ((key * 2862933555777941757) + 1) & 0xffffffffffffffff
        j = float(b + 1) * (float(1 << 31) / float((key >> 33) + 1))

    return int(b)
