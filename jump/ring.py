
"""Hash ring using Jump Consistent Hash."""

import binascii
import bisect

import jump


def _crc32(data):
    return binascii.crc32(data.encode('ascii')) & 0xffffffff


class NoNodeError(Exception):
    """No no present in ring."""


class DuplicateNodeError(Exception):
    """Node already present in ring."""


class HashRing(object):

    def __init__(self, nodes=None, hasher=_crc32):
        if not nodes:
            raise ValueError('nodes must not be empty')

        self._nodes = sorted(nodes)
        self._hasher = hasher

    def get_node(self, node):
        try:
            i = jump.hash(self._hasher(node), len(self._nodes))
        except ValueError:
            raise NoNodeError('no nodes present in ring')
        return self._nodes[i]

    def add_node(self, node):
        if node in self._nodes:
            raise DuplicateNodeError('node %r already present at index %d' %
                                     (node, self._nodes.index(node)))
        bisect.insort(self._nodes, node)

    def remove_node(self, node):
        self.__delitem__(node)

    def __getitem__(self, key):
        return self._nodes.__getitem__(key)

    def __delitem__(self, node):
        self._nodes.remove(node)

    def __contains__(self, node):
        return self._nodes.__contains__(node)

    def __iter__(self):
        for node in self._nodes.__iter__():
            yield node

    def __len__(self):
        return self._nodes.__len__()

    def __str__(self):
        return self._nodes.__str__()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._nodes)

    def __lt__(self, other):
        return self._nodes.__lt__(other)

    def __le__(self, other):
        return self._nodes.__le__(other)

    def __eq__(self, other):
        return self._nodes.__eq__(other)

    def __ne__(self, other):
        return self._nodes.__ne__(other)

    def __gt__(self, other):
        return self._nodes.__gt__(other)

    def __ge__(self, other):
        return self._nodes.__ge__(other)
