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
        self.atom = atom

    def __repr__(self):
        return 'Atom(%s)' % repr(self.atom)

    def __str__(self):
        return str(self.atom)

    def __len__(self):
        return len(self.atom)

    def __hash__(self):
        return hash(self.atom)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.atom == other.atom
        return self.atom == other

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        return str(self.atom)

    def isflat(self):
        return True


class BaseList(AbstractBaseLispNode):
    """Base list class."""
    node_name = 'BaseList'

    def __init__(self, inner_nodes):
        AbstractBaseLispNode.__init__(self)
        self.children = list(inner_nodes)
        self._func = None if len(inner_nodes) == 0 else inner_nodes[0]

        self.nested = False
        for _ in self.children:
            if not _.isflat():
                self.nested = True
                break
        if not self.nested:
            self.generator = self.flat_generator
        else:
            self.generator = self.nested_generator

    def __repr__(self):
        return '%s(%s)' % (
            str(self.node_name), (', '.join(repr(_) for _ in self.children)))

    def __len__(self):
        return len(self.children)

    def __getitem__(self, k):
        return self.children[k]

    def __eq__(self, other):
        if isinstance(other, BaseList):
            return self.children == other.children
        return self.children == list(other)

    def __hash__(self):
        return hash(repr(self.children))

    def __iter__(self):
        return iter(self.children)

    def isflat(self):
        return not self.children

    flat_generator = dummy_flat_generator
    nested_generator = dummy_nested_generator

# Specialized list classes


class List(BaseList):
    node_name = 'List'

    def pprint(self, options=DEFAULT_OPTIONS.copy()):
        generator = zip(
            self.generator(), self.children, self.offset_generator())
        result = []
        for prefix, node, offset in generator:
            node.offset = offset
            result.extend((prefix, node.pprint(options)))
        return '(%s)' % ''.join(result)

    def offset_generator(self):
        for _ in range(len(self.children) + 1):
            yield self.offset + 2

    flat_generator = default_flat_generator
    nested_generator = default_nested_generator


class FirstBraceAlignList(List, BaseList):
    node_name = 'FirstBraceAlignList'
    nested_generator = first_brace_align_generator


class FunctionAlignList(List, BaseList):
    node_name = 'FunctionAlignList'

    def offset_generator(self):
        for _ in range(len(self.children) + 1):
            yield self.offset + 2 + len(self._func)

    nested_generator = function_align_generator

# Named Lists


class LetList(List, BaseList):
    """Let object."""

    def __init__(self, inner_nodes):
        BaseList.__init__(self, inner_nodes)
        self.children[1] = FirstBraceAlignList(self.children[1])
        self.generator = self.flat_generator

    node_name = 'LetList'

    def flat_generator(self):
        yield ''
        yield ' '
        value = '\n' + ' ' * (self.offset + 2)
        for _ in range(len(self.children) - 2):
            yield value
        yield ''

    def offset_generator(self):
        yield 0
        yield self.offset + len(self._func) + 2
        for _ in range(len(self.children) - 2):
            yield self.offset + 2


class IfList(List, BaseList):
    """If object."""

    def __init__(self, inner_nodes):
        BaseList.__init__(self, inner_nodes)
        self.generator = self.flat_generator

    node_name = 'IfList'

    def flat_generator(self):
        yield ''
        yield ' '
        yield '\n' + ' ' * (self.offset + 4)
        value = '\n' + ' ' * (self.offset + 2)
        for _ in range(len(self.children) - 3):
            yield value
        yield ''

    def offset_generator(self):
        yield 0
        yield self.offset + len(self._func) + 2
        yield self.offset + len(self._func) + 2
        for _ in range(len(self.children) - 3):
            yield self.offset + 2


class DefunList(List, BaseList):
    """Defun object."""

    def __init__(self, inner_nodes):
        List.__init__(self, inner_nodes)
        self.generator = self.flat_generator

    node_name = 'DefunList'

    def flat_generator(self):
        value = '\n' + ' ' * (self.offset + 2)
        yield ''
        yield ' '
        yield ' '
        for _ in range(len(self.children) - 3):
            yield value
        yield ''

    def offset_generator(self):
        yield 0
        offset = self.offset + len(self._func) + 2
        yield offset
        yield offset + len(self.children[1]) + 2
        offset = self.offset + 2
        for _ in range(len(self.children) - 3):
            yield offset


class SetfList(List, BaseList):
    """Setf object."""

    def __init__(self, inner_nodes):
        List.__init__(self, inner_nodes)
        self.generator = self.flat_generator

    node_name = 'SetfList'

    def flat_generator(self):
        value = '\n' + ' ' * (self.offset + 2 + len(self._func))
        yield ''
        yield ' '
        yield ' '
        for _ in range((len(self.children) - 3) // 2):
            yield value
            yield ' '
        yield value

    def offset_generator(self):
        yield 0
        offset = self.offset + len(self._func) + 2
        for i in range((len(self.children) - 1) // 2):
            yield offset
            yield offset + len(self.children[1 + 2 * i]) + 1
        yield offset


NODES = {
    'and': FunctionAlignList,
    'defun': DefunList,
    'setf': SetfList,
    'eq': FunctionAlignList,
    'if': IfList,
    'let': LetList,
    'let*': LetList,
    'or': FunctionAlignList,
}


def wrap_list(node):
    return NODES.get(
        node[0], List if node[0].isflat() else FirstBraceAlignList
    )(node) if node else List(node)
