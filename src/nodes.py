#! /usr/bin/env python3

from .tools import abstractmethod

class AbstractBaseLispNode:

    @abstractmethod
    def pprint(self):
        return 'AbstractMethod'



class Atom(AbstractBaseLispNode):

    def __init__(self, atom):
        self._atom = atom

    def __repr__(self):
        return 'Atom(%s)' % repr(self._atom)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self._atom == other._atom
        return self._atom == other

    def pprint(self):
        return repr(self._atom)


class List(AbstractBaseLispNode):

    def __init__(self, inner_nodes):
        self._nodes = tuple(inner_nodes)

    def __repr__(self):
        return 'List(%s)' % (', '.join(repr(_) for _ in self._nodes))

    def __eq__(self, other):
        if isinstance(other, List):
            return self._nodes == other._nodes
        return self._nodes == tuple(other)
