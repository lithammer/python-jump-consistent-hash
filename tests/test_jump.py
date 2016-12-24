from unittest import TestCase

import jump


class JumpConsistentHashTestCase(TestCase):

    def test_hash(self):
        h = jump.py_hash(1, 1)
        self.assertEqual(h, 0)

        h = jump.py_hash(42, 57)
        self.assertEqual(h, 43)

        h = jump.py_hash(0xDEAD10CC, 1)
        self.assertEqual(h, 0)

        h = jump.py_hash(0xDEAD10CC, 666)
        self.assertEqual(h, 361)

        h = jump.py_hash(256, 1024)
        self.assertEqual(h, 520)

    def test_negative_bucket_number(self):
        self.assertRaises(ValueError, jump.py_hash, 0, -10)
        self.assertRaises(ValueError, jump.py_hash, 0xDEAD10CC, -666)


class JumpConsistentHashExtensionTestCase(TestCase):

    def test_hash(self):
        h = jump.c_hash(1, 1)
        self.assertEqual(h, 0)

        h = jump.c_hash(42, 57)
        self.assertEqual(h, 43)

        h = jump.c_hash(0xDEAD10CC, 1)
        self.assertEqual(h, 0)

        h = jump.c_hash(0xDEAD10CC, 666)
        self.assertEqual(h, 361)

        h = jump.c_hash(256, 1024)
        self.assertEqual(h, 520)

    def test_negative_bucket_number(self):
        self.assertRaises(ValueError, jump.c_hash, 0, -10)
        self.assertRaises(ValueError, jump.c_hash, 0xDEAD10CC, -666)
