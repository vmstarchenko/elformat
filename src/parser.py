#! /usr/bin/env python3

"""Parser."""

from .lispstream import LispStream, LispSyntaxError
from .nodes import Program, Atom, Comment, wrap_list


class StackElement(list):
    """Wrapper for raw lisp nodes.

    Can separate comments from source code.

    """

    def __init__(self, open_brace=None, close_brace=None):
        super(StackElement, self).__init__(self)
        self.comments = dict()
        self.open_brace = '(' if open_brace is None else open_brace
        self.close_brace = ')' if close_brace is None else close_brace

    def add(self, atom):
        """Add atom to current list.

        Check if atom is comment. If true add comment after last current
        element. If false add atom at the end of list.

        """
        if atom and atom[0] == ';':
            length = self.__len__()
            if length in self.comments:
                self.comments[length].append(Comment(atom))
            else:
                self.comments[length] = [Comment(atom), ]
        else:
            self.append(Atom(atom))


class Stack(list):
    """Stack class with wrappers of some default list functions."""

    def __init__(self):
        super(Stack, self).__init__()
        self.append(StackElement())

    @property
    def top(self):
        """Top element."""
        return self[-1]

    def push_new(self):
        """Create new stack element and push it to the top."""
        self.append(StackElement())

    def pop(self):
        if self.__len__() <= 1:
            raise LispSyntaxError('extra brace')

        wrapped = wrap_list(super(Stack, self).pop())
        self[-1].append(wrapped)
        return wrapped



def parse(string):
    """Try to parse string and return Node object."""

    stream = LispStream(string)
    stack = Stack()
    while stream:
        stream.skip()
        char = stream.get(False)
        if char == '(':                             # create new node
            stack.push_new()
            stream.get()
        elif char == ')':                           # finish current node
            stack.pop()
            stream.get()
        elif char == '"':                           # create string atom
            string = stream.read_string()
            if string is None:
                raise LispSyntaxError(
                    "can't read string at position %s" % stream.get_state())
            stack.top.add(string)
        elif char == ';':
            comment = stream.read_comment()
            print('comment', comment)
            if comment is None:
                raise LispSyntaxError(
                    "can't read string at position %s" % stream.get_state())
            stack.top.add(comment)
        else:                                       # create any another atom
            atom = stream.read_atom()
            if atom is None:
                raise LispSyntaxError(
                    "can't read atom at position %s" % stream.get_state())

            stack.top.add(atom)

    if len(stack) > 1:
        raise LispSyntaxError('unclosed brace')

    return Program(stack.top)
