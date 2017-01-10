#! /usr/bin/env python3

from .tools import abstractmethod
from .generators import (
    dummy_nested_generator, dummy_flat_generator,
    default_flat_generator, default_nested_generator,
    first_brace_align_generator,
    function_align_generator,
    function_align_generator_1,
    function_align_generator_2,
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
        super(Atom, self).__init__()
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

    def __init__(self, children):
        super(BaseList, self).__init__()
        self.children = list(children)
        self._func = None if len(children) == 0 else children[0]

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
        generator = zip(self.generator(), self.children)
        result = []
        for (prefix, offset), node in generator:
            node.offset = offset
            result.extend((prefix, node.pprint(options)))
        return '(%s)' % ''.join(result)

    flat_generator = default_flat_generator
    nested_generator = default_nested_generator


class FirstBraceAlignList(List):
    node_name = 'FirstBraceAlignList'
    nested_generator = first_brace_align_generator


class FunctionAlignList(List):
    node_name = 'FunctionAlignList'

    nested_generator = function_align_generator

def generate_node_class(node_name, flat_generator, nested_generator=None):
    """
    Create node class using template:

    class NewClass(List):
        __doc__ = "{node_name} object."

        node_name = node_name

        flat_generator = flat_generator
        nested_generator = nested_generator
        offset_generator = offset_generator

    if nested_generator is None set flat_generator as nested_generator
    """

    nested_generator = nested_generator or flat_generator
    node_name = node_name.replace(' ', '_')
    return type(node_name+'List',
                (List,),
                {
                    '__doc__': '%s object.' % str(node_name),
                    'flat_generator': flat_generator,
                    'nested_generator': nested_generator
                })

# Named Lists


class LetList(List):
    """Let object."""
    node_name = 'LetList'

    def __init__(self, children):
        super(LetList, self).__init__(children)
        self.children[1] = FirstBraceAlignList(self.children[1])
        self.generator = self.flat_generator

    flat_generator = function_align_generator_1


class DefunList(List):
    """Defun object."""

    def __init__(self, children):
        super(DefunList, self).__init__(children)
        self.generator = self.flat_generator

    node_name = 'DefunList'

    def flat_generator(self):
        yield ('', 0)
        offset = self.offset + len(self._func) + 2
        yield (' ', offset)
        yield (' ', offset + len(self.children[1]) + 2)
        offset = self.offset + 2
        value = ('\n' + ' ' * (self.offset + 2), offset)
        for _ in range(len(self.children) - 3):
            yield value
        yield ('', 0)


class SetfList(List):
    """Setf object."""

    def __init__(self, children):
        super(SetfList, self).__init__(children)
        self.generator = self.flat_generator

    node_name = 'SetfList'

    def flat_generator(self):
        offset = self.offset + len(self._func) + 2
        value = ('\n' + ' ' * (self.offset + 2 + len(self._func)),
                 offset)
        yield ('', 0)
        yield (' ', offset)
        yield (' ', offset + len(self.children[1]) + 1)
        for i in range((len(self.children) - 3) // 2):
            yield value
            yield (' ', offset + len(self.children[1 + 2 * i]) + 1)
        yield value

DolistList = generate_node_class(
    'Dolist',
    function_align_generator_1)

IfList = generate_node_class(
    'If',
    function_align_generator_2)

NODES = {
    'and': FunctionAlignList,
    'defun': DefunList,
    'dolist': DolistList,
    'eq': FunctionAlignList,
    'eql': FunctionAlignList,
    'equal': FunctionAlignList,
    'if': IfList,
    'let': LetList,
    'let*': LetList,
    'or': FunctionAlignList,
    'setf': SetfList,
    # 'lambda': DefunList,
}


def wrap_list(node):
    return NODES.get(
        node[0], List if node[0].isflat() else FirstBraceAlignList
    )(node) if node else List(node)
