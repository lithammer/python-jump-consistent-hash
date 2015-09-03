import unittest

from jump.ring import HashRing, DuplicateNodeError, NoNodeError


class TestHashRing(unittest.TestCase):

    def setUp(self):
        self.ring = HashRing(['a', 'b', 'c'])

    def test_ensure_nodes(self):
        """Verify that HashRing can't be created with empty list."""
        self.assertRaises(ValueError, HashRing, [])

    def test_ring_length(self):
        self.assertEqual(len(self.ring), 3)

    def test_add_node(self):
        self.ring.add_node('d')
        self.assertEqual(len(self.ring), 4)
        self.assertIn('d', self.ring)

    def test_get_one_node(self):
        ring = HashRing(['a'])
        self.assertEqual(ring.get_node('foo'), 'a')

    def test_get_node(self):
        tests = [
            ('foo', 'c'),
            ('bar', 'b'),
            ('baz', 'a'),
            ('qux', 'a')
        ]

        for key, expect in tests:
            for _ in range(10):
                self.assertEqual(self.ring.get_node(key),  expect)

        for c in 'abcdefghijklmopqrstuvwxyz':
            self.assertIn(self.ring.get_node(c), ['a', 'b', 'c'])

    def test_remove_node(self):
        """Verify that nodes are removed correctly."""
        del self.ring['a']
        self.assertEqual(len(self.ring), 2)
        self.assertEqual(self.ring._nodes, ['b', 'c'])

        self.ring.remove_node('b')
        self.assertEqual(len(self.ring), 1)
        self.assertEqual(self.ring._nodes, ['c'])

    def test_add_duplicate_node(self):
        """Verify that inserting a duplicate node raises an exception."""
        self.assertRaises(DuplicateNodeError, self.ring.add_node, 'a')

    def test_sorted_insert(self):
        """Verify that added nodes gets sorted."""
        ring = HashRing(['b', 'd', 'f'])

        tests = [
            ('a', ['a', 'b', 'd', 'f']),
            ('c', ['a', 'b', 'c', 'd', 'f']),
            ('e', ['a', 'b', 'c', 'd', 'e', 'f'])
        ]

        for node, expect in tests:
            ring.add_node(node)
            self.assertEqual(ring, expect)
            self.assertNotEqual(ring, reversed(expect))

    def test_empty_ring(self):
        """Verify that getting a node in an empty ring raises an exception."""
        map(self.ring.remove_node, 'abc')
        self.assertRaises(NoNodeError, self.ring.get_node, 'a')
