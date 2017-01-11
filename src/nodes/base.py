#! /usr/bin/env python3


"""Base classes ans function for nodes."""


__all__ = ('FunctionAlignList', 'List', 'FirstBraceAlignList',
           'Atom', 'Comment', 'Program')

from src.tools import abstractmethod
from src.generators import (
    dummy_nested_generator, dummy_flat_generator,
    default_flat_generator, default_nested_generator,
    first_brace_align_generator,
    function_align_generator
)


class Atom:
    """Base atom class."""

    def __init__(self, atom):
        self.offset = 0
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

    def pprint(self):
        """Pretty form of lisp Node."""
        return str(self.atom)

    @property
    def isflat(self):
        """Atom always is flat."""
        return True


class Comment:
    """Base comment class."""

    def __init__(self, comment):
        self.offset = 0
        self.comment_level = 0
        for _ in comment:
            if _ == ';':
                self.comment_level += 1
            else:
                break
        self.comment = comment[self.comment_level:].strip()

    def __repr__(self):
        return 'Comment(%s %s)' % (';' * self.comment_level, repr(self.comment),)

    def __str__(self):
        return '%s %s' % (';' * self.comment_level, str(self.comment),)

    def __len__(self):
        return len(self.comment) + 1 + self.comment_level

    def __hash__(self):
        return hash((self.comment, self.comment_level))

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.comment == other.comment and \
                self.comment_level == other.comment_level
        return str(self.comment) == str(other)

    def pprint(self):
        """Pretty form of lisp Node."""
        if self.comment_level == 1:
            return ' ; %s' % (str(self.comment),)
        elif self.comment_level == 2:
            return '\n%s;; %s' % (
                ' ' * self.offset, str(self.comment),)
        else:
            return '\n%s %s' % (
                ';' * self.comment_level, str(self.comment).capitalize(),)

    @property
    def isflat(self):
        """Comment always is nested."""
        return False


class BaseList:
    """Base list class."""
    node_name = 'BaseList'

    def __init__(self, children, comments=None):
        self.offset = 0
        self.children = list(children)
        self.func = None if len(children) == 0 else children[0]
        self.comments = comments or dict()

        self.nested = False
        for _ in self.children:
            if not _.isflat:
                self.nested = True
                break
        if not self.nested:
            for comments in self.comments.values():
                for _ in comments:
                    print(repr(_))
                    if not _.isflat:
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

    @property
    def isflat(self):
        """Check if list is flat.

        List is flat if it's nil.

        """
        return not self.children

    @abstractmethod
    def pprint(self):
        """Pretty form of lisp Node."""
        pass

    flat_generator = dummy_flat_generator
    nested_generator = dummy_nested_generator

# Specialized list classes


class List(BaseList):
    """Default class for usual list, base class for named lists."""
    node_name = 'List'

    def pprint(self):
        generator = zip(self.generator(), self.children,
                        range(len(self.children) + 1))
        result = []
        for (prefix, offset), node, i in generator:
            node.offset = offset
            if i in self.comments:
                for comment in self.comments[i]:
                    comment.offset = offset
                    result.append(comment.pprint())
            result.extend((prefix, node.pprint()))
        return '(%s)' % ''.join(result)

    flat_generator = default_flat_generator
    nested_generator = default_nested_generator


def generate_node_class(node_name, flat_generator=None, nested_generator=None):
    """Create node class using template:

    class NewClass(List):
        __doc__ = "{node_name} object."

        node_name = node_name

        flat_generator = flat_generator
        nested_generator = nested_generator
        offset_generator = offset_generator

    if nested_generator is None use default_flat_generator
    if nested_generator is None use flat_generator

    """

    flat_generator = flat_generator or default_flat_generator
    nested_generator = nested_generator or flat_generator
    node_name = node_name.replace(' ', '_')
    return type(node_name + 'List',
                (List,),
                {
                    '__doc__': '%s object.' % str(node_name),
                    'flat_generator': flat_generator,
                    'nested_generator': nested_generator
                })


class FirstBraceAlignList(List):
    """Node wrapper for first brace aligned lists."""
    node_name = 'FirstBraceAlignList'
    nested_generator = first_brace_align_generator


class FunctionAlignList(List):
    """Node wrapper for function aligned lists."""
    node_name = 'FunctionAlignList'
    nested_generator = function_align_generator


class Program(BaseList):
    """Programm."""
    node_name = 'Programm'

    def pprint(self):
        generator = zip(self.generator(), self.children,
                        range(len(self.children) + 1))
        result = []
        for (prefix, offset), node, i in generator:
            node.offset = offset
            if i in self.comments:
                for comment in self.comments[i]:
                    comment.offset = offset
                    result.append(comment.pprint())
            result.extend((prefix, node.pprint()))
        return ''.join(result)

    def flat_generator(self):
        yield ('', 0)
        value = ('\n', 0)
        for _ in range(len(self.children) - 1):
            yield value
        yield ('', 0)

    nested_generator = flat_generator
