#! /usr/bin/env python3

# pylint: disable=C0103

"""Specified nodes."""

from src.generators import function_align_generator_1, function_align_generator_2
from .base import List, FirstBraceAlignList, generate_node_class


class LetList(List):
    """Let object."""
    node_name = 'LetList'

    def __init__(self, children, *args, **kargs):
        super(LetList, self).__init__(children, *args, **kargs)
        self.children[1] = FirstBraceAlignList(self.children[1])
        self.generator = self.flat_generator

    flat_generator = function_align_generator_1


class DefunList(List):
    """Defun object."""

    def __init__(self, children, *args, **kargs):
        super(DefunList, self).__init__(children, *args, **kargs)
        self.generator = self.flat_generator

    node_name = 'DefunList'

    def flat_generator(self):
        """Generator.

        +--------------------------------------------------------------+
        | (defun (arguments)                                           |
        |   body)                                                      |
        +--------------------------------------------------------------+

        """
        yield ('', self.offset + 1)
        offset = self.offset + len(self.func) + 2
        yield (' ', offset)
        yield (' ', offset + len(self.children[1]) + 2)
        offset = self.offset + 2
        value = ('\n' + ' ' * (self.offset + 2), offset)
        for _ in range(len(self.children) - 3):
            yield value
        yield ('', 0)


class SetfList(List):
    """Setf object."""

    def __init__(self, children, *args, **kargs):
        super(SetfList, self).__init__(children, *args, **kargs)
        self.generator = self.flat_generator

    node_name = 'SetfList'

    def flat_generator(self):
        """Generator.

        +--------------------------------------------------------------+
        | (setf key value                                              |
        |       key value)                                             |
        |       ...)                                                   |
        +--------------------------------------------------------------+

        """
        offset = self.offset + len(self.func) + 2
        value = ('\n' + ' ' * (self.offset + 2 + len(self.func)),
                 offset)
        yield ('', self.offset + 1)
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
