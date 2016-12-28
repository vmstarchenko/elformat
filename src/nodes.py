#! /usr/bin/env python3

from .tools import abstractmethod


class AbstractBaseLispNode:
    """Base lisp node class."""

    @abstractmethod
    def pprint(self, depth=0):
        """Pretty form of lisp Node."""
        pass


class Atom(AbstractBaseLispNode):
    """Base atom class."""

    def __init__(self, atom):
        self._atom = atom

    def __repr__(self):
        return 'Atom(%s)' % repr(self._atom)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self._atom == other._atom
        return self._atom == other

    def pprint(self, depth=0):
        return str(self._atom)


class List(AbstractBaseLispNode):
    """Base list class."""

    def __init__(self, inner_nodes):
        self._nodes = tuple(inner_nodes)
        self._func = None if len(inner_nodes) == 0 else inner_nodes[0]

    def __repr__(self):
        return 'List(%s)' % (', '.join(repr(_) for _ in self._nodes))

    def __eq__(self, other):
        if isinstance(other, List):
            return self._nodes == other._nodes
        return self._nodes == tuple(other)

    def pprint(self, depth=0):
        return '(%s)' % ' '.join(_.pprint(depth + 1) for _ in self._nodes)

# Specialized list classes


class LetList(List):
    """Let object."""

    def pprint(self, depth=0):
        line = '(%s (' % self._func
        line += (' ' * len(line)).join(_.pprint(0) for _ in self._nodes[1])
        line += ')'
        result = [line, ]
        result.extend((_.pprint(depth + 1) for _ in self._nodes[2:]))

        return ('\n  ' * depth).join(result)

NODES = {
    'let': LetList,
    'let*': LetList
}


def wrap_list(node):
    return NODES.get(node, List)(node) if node else List(node)
