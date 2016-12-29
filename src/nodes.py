#! /usr/bin/env python3

from .tools import abstractmethod
from .generators import (
    dummy_nested_generator, dummy_flat_generator,
    default_flat_generator, default_nested_generator,
    first_brace_align_generator, function_align_generator
)

DEFAULT_OPTIONS = {
    'line_width': 80,
}


class AbstractBaseLispNode:
    """Base lisp node class."""

    def __init__(self):
        self.offset = 0

    @abstractmethod
    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        """Pretty form of lisp Node."""
        pass


class Atom(AbstractBaseLispNode):
    """Base atom class."""

    def __init__(self, atom):
        AbstractBaseLispNode.__init__(self)
        self._atom = atom

    def __repr__(self):
        return 'Atom(%s)' % repr(self._atom)

    def __str__(self):
        return str(self._atom)

    def __len__(self):
        return len(self._atom)

    def __hash__(self):
        return hash(self._atom)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self._atom == other._atom
        return self._atom == other

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        return str(self._atom)

    def isflat(self):
        return True


class BaseList(AbstractBaseLispNode):
    """Base list class."""
    node_name = 'BaseList'

    def __init__(self, inner_nodes):
        AbstractBaseLispNode.__init__(self)
        self._nodes = list(inner_nodes)
        self._func = None if len(inner_nodes) == 0 else inner_nodes[0]

        self.nested = False
        for _ in self._nodes:
            if not _.isflat():
                self.nested = True
                break
        if not self.nested:
            self.generator = self.flat_generator
        else:
            self.generator = self.nested_generator

    def __repr__(self):
        return '%s(%s)' % (
            str(self.node_name), (', '.join(repr(_) for _ in self._nodes)))

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, k):
        return self._nodes[k]

    def __eq__(self, other):
        if isinstance(other, BaseList):
            return self._nodes == other._nodes
        return self._nodes == list(other)

    def __hash__(self):
        return hash(repr(self._nodes))

    def __iter__(self):
        return iter(self._nodes)

    def isflat(self):
        return not self._nodes

    flat_generator = dummy_flat_generator
    nested_generator = dummy_nested_generator

# Specialized list classes


class List(BaseList):

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        absolute_offset = self.get_absolute_offset()
        result = []
        for prefix, node in zip(
                self.generator(), self._nodes):
            node.offset = absolute_offset
            result.extend((prefix, node.pprint(options)))
        return '(%s)' % ''.join(result)

    def get_absolute_offset(self):
        return self.offset + 2

    flat_generator = default_flat_generator
    nested_generator = default_nested_generator


class FirstBraceAlignList(List, BaseList):
    nested_generator = first_brace_align_generator


class FunctionAlignList(List, BaseList):

    def get_absolute_offset(self):
        return self.offset + 2 + len(self._func)

    nested_generator = function_align_generator

# Named Lists


class LetList(List, BaseList):
    """Let object."""

    def __init__(self, inner_nodes):
        BaseList.__init__(self, inner_nodes)
        self._nodes[1] = FirstBraceAlignList(self._nodes[1])
        self.generator = self.flat_generator

    node_name = 'LetList'

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        generator = zip(self.generator(), self._nodes)
        result = []

        prefix, node = next(generator)
        result.extend((prefix, node.pprint(options)))

        prefix, node = next(generator)
        node.offset = self.offset + len(self._func) + 3
        result.extend((prefix, node.pprint(options)))

        for prefix, node in generator:
            # set generators
            node.offset = self.offset + 2
            result.extend((prefix, node.pprint(options)))
        return '(%s)' % ''.join(result)

    def flat_generator(self):
        yield ''
        yield ' '
        value = '\n' + ' ' * (self.offset + 2)
        for _ in range(len(self._nodes) - 2):
            yield value
        yield ''


NODES = {
    'let': LetList,
    'let*': LetList,
    'and': FunctionAlignList,
    'or': FunctionAlignList,
}


def wrap_list(node):
    return NODES.get(node[0], List)(node) if node else BaseList(node)
