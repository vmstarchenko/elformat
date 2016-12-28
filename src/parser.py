#! /usr/bin/env python3

from .lispstream import LispStream
from .nodes import Atom, List, wrap_list


class LispSyntaxError(ValueError):
    """Error for not valid lisp programms."""
    pass


def parse(string):
    stream = LispStream(string)
    stack = [[], ]
    while stream:
        stream.skip()
        char = stream.get(False)
        if char == '(':
            stack.append([])
            stream.get()
        elif char == ')':
            last = stack.pop()
            if not stack:
                raise LispSyntaxError('extra brace')
            stack[-1].append(wrap_list(last))
            stream.get()
        elif char == '"':
            string = stream.read_string()
            if string is None:
                raise LispSyntaxError(
                    "can't read string at position %s" % stream.get_state())
            stack[-1].append(Atom(string))
        else:
            atom = stream.read_atom()
            if atom is None:
                raise LispSyntaxError(
                    "can't read atom at position %s" % stream.get_state())
            stack[-1].append(Atom(atom))
    if len(stack) > 1:
        raise LispSyntaxError('unclosed brace')
    return stack[0]
