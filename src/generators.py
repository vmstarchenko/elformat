#! /usr/bin/env python3

from .tools import abstractmethod

@abstractmethod
def dummy_nested_generator(node):
    """Dummy for abstract nodes."""
    pass


@abstractmethod
def dummy_flat_generator(node):
    """Dummy for abstract nodes."""
    pass


def default_flat_generator(node):
    """Generator.

    +------------------------------------------------------------------+
    | (func arg1 arg2)                                                 |
    +------------------------------------------------------------------+

    """
    yield ''
    for _ in range(len(node.children) - 1):
        yield ' '
    yield ''


def default_nested_generator(node):
    """Generator.

    +------------------------------------------------------------------+
    | (func                                                            |
    |   arg1                                                           |
    |   arg2)                                                          |
    +------------------------------------------------------------------+

    """
    yield ''
    value = '\n' + ' ' * (node.offset + 2)
    for _ in range(len(node.children) - 1):
        yield value
    yield '\n'


def first_brace_align_generator(node):
    """Generator.

    +------------------------------------------------------------------+
    | (arg0                                                            |
    |  arg1                                                            |
    |  arg2)                                                           |
    +------------------------------------------------------------------+

    """
    yield ''
    value = '\n' + ' ' * (node.offset + 1)
    for _ in range(len(node.children) - 1):
        yield value
    yield ''


def function_align_generator(node):
    """Generator.

    +------------------------------------------------------------------+
    | (func arg1                                                       |
    |       arg2                                                       |
    |       arg3)                                                      |
    +------------------------------------------------------------------+

    """
    offset = node.offset + 2 + len(node._func)
    yield ''
    yield ' '
    value = '\n' + ' ' * offset
    for _ in range(len(node.children) - 2):
        yield value
    yield ''
