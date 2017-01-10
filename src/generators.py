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
    offset = node.offset + 2
    yield ('', offset)
    value = (' ', offset)
    for _ in range(len(node.children) - 1):
        yield value
    yield ('', offset)


def default_nested_generator(node):
    """Generator.

    +------------------------------------------------------------------+
    | (func                                                            |
    |   arg1                                                           |
    |   arg2)                                                          |
    +------------------------------------------------------------------+

    """
    offset = node.offset + 2
    yield ('', offset)
    value = ('\n' + ' ' * (node.offset + 2), offset)
    for _ in range(len(node.children) - 1):
        yield value
    yield ('\n', offset)


def first_brace_align_generator(node):
    """Generator.

    +------------------------------------------------------------------+
    | (arg0                                                            |
    |  arg1                                                            |
    |  arg2)                                                           |
    +------------------------------------------------------------------+

    """
    offset = node.offset + 2
    yield ('', offset)
    value = ('\n' + ' ' * (node.offset + 1), offset)
    for _ in range(len(node.children) - 1):
        yield value
    yield ('', offset)


def function_align_generator_f(n):
    """Fabric of generators.

    Create generators with arguments align by function. If n is None
    align all arguments by function else align first n by function
    and use default indentation for other.

    +------------------------------------------------------------------+
    | (func arg_1                                                      |
    |       ...                                                        |
    |       arg_n                                                      |
    |   arg_n+1                                                        |
    |   ...)                                                           |
    +------------------------------------------------------------------+

    """
    if n is None:
        def newfunc(node):
            offset = node.offset + 2 + len(node._func)
            yield ('', 0)
            yield (' ', offset)
            value = ('\n' + ' ' * offset, offset)
            for _ in range(len(node.children) - 2):
                yield value
            yield ('', offset)
        return newfunc
    else:
        def newfunc(node):
            offset = node.offset + 2 + len(node._func)
            yield ('', 0)
            yield (' ', offset)
            value = ('\n' + ' ' * offset, offset)
            for _ in range(n - 1):
                yield value
            offset = node.offset + 2
            value = ('\n' + ' ' * offset, offset)
            for _ in range(len(node.children) - n - 1):
                yield value
            yield ('', 0)
    return newfunc

function_align_generator = function_align_generator_f(None)
