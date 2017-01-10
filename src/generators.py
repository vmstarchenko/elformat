#! /usr/bin/env python3


"""Contains all base generators for nodes

Generator return pair (prefix, offset)
prefix is a string that would be insert before node
offset is a int value that would be set as node offset

for list with n nodes generator must return n+1 value because
first value is for place before first node and last value
is for place after last node.

"""

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
            """Align arguments by function name"""
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
        setattr(newfunc, '__doc__', 'Align first %d arguments by function name' %n)
    return newfunc

function_align_generator = function_align_generator_f(None)
function_align_generator_1 = function_align_generator_f(1)
function_align_generator_2 = function_align_generator_f(2)
function_align_generator_3 = function_align_generator_f(3)
function_align_generator_4 = function_align_generator_f(4)
