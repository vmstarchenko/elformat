#! /usr/bin/env python3

from .tools import abstractmethod

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


class List(AbstractBaseLispNode):
    """Base list class."""
    node_name = 'List'

    def __init__(self, inner_nodes):
        AbstractBaseLispNode.__init__(self)
        self._nodes = list(inner_nodes)
        self._func = None if len(inner_nodes) == 0 else inner_nodes[0]

        nested = False
        for _ in self._nodes:
            if not _.isflat():
                nested = True
                break
        if not nested:
            self.offset_generator = self.flat_offset_generator
            self.newline_generator = self.flat_newline_generator
        else:
            self.offset_generator = self.nested_offset_generator
            self.newline_generator = self.nested_newline_generator

    def __repr__(self):
        return '%s(%s)' % (str(self.node_name), (', '.join(repr(_) for _ in self._nodes)))

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, k):
        return self._nodes[k]

    def __eq__(self, other):
        if isinstance(other, List):
            return self._nodes == other._nodes
        return self._nodes == list(other)

    def __hash__(self):
        return hash(repr(self._nodes))

    def __iter__(self):
        return iter(self._nodes)

    def isflat(self):
        return False

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        result = []
        for offset, newline, node in zip(
                self.offset_generator(), self.newline_generator(), self._nodes):
            # set generators
            node.offset = self.offset + 2
            result.extend(('\n' * newline, ' ' * offset, node.pprint(options)))
        return '(%s)' % ''.join(result)

    def flat_offset_generator(self):
        yield 0
        for _ in range(len(self._nodes) - 1):
            yield 1
        yield 0

    def flat_newline_generator(self):
        for _ in range(len(self._nodes) + 1):
            yield 0

    def nested_offset_generator(self):
        yield 0
        for _ in range(len(self._nodes) - 1):
            yield self.offset + 2
        yield 0

    def nested_newline_generator(self):
        yield 0
        for _ in range(len(self._nodes)):
            yield 1


# Specialized list classes


class LetList(List):
    """Let object."""

    def __init__(self, inner_nodes):
        List.__init__(self, inner_nodes)
        self._nodes[1] = LetListSetField(self._nodes[1])
        self._func = None if len(inner_nodes) == 0 else inner_nodes[0]

    node_name = 'LetList'

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        generator = zip(self.flat_offset_generator(),
                        self.flat_newline_generator(), self._nodes)
        result = []

        offset, newline, node = next(generator)
        result.extend(('\n' * newline, ' ' * offset, node.pprint(options)))

        offset, newline, node = next(generator)
        node.offset = self.offset + len(self._func) + 3
        result.extend(('\n' * newline, ' ' * offset, node.pprint(options)))

        for offset, newline, node in generator:
            # set generators
            node.offset = self.offset + 2
            result.extend(('\n' * newline, ' ' * offset, node.pprint(options)))
        return '(%s)' % ''.join(result)

    def flat_offset_generator(self):
        yield 0
        yield 1
        for _ in range(len(self._nodes) - 2):
            yield self.offset + 2
        yield 0

    def flat_newline_generator(self):
        yield 0
        yield 0
        for _ in range(len(self._nodes) - 2):
            yield 1
        yield 0


class LetListSetField(List):
    def flat_offset_generator(self):
        yield 0
        for _ in range(len(self._nodes) - 1):
            yield self.offset
        yield 0

    def flat_newline_generator(self):
        yield 0
        for _ in range(len(self._nodes) - 1):
            yield 1
        yield 0

    nested_offset_generator = flat_offset_generator
    nested_newline_generator = flat_newline_generator

NODES = {
    'let': LetList,
    'let*': LetList
}


def wrap_list(node):
    return NODES.get(node[0], List)(node) if node else List(node)
