#! /usr/bin/env python3

"""Wrappers for lisp source code nodes.

Each node responsible for it's appearance

"""

from .named_nodes import IfList, LetList, DefunList, DolistList, SetfList
from .base import FunctionAlignList, List, FirstBraceAlignList, Atom

__all__ = ('wrap_list', 'Atom',)

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
}


def wrap_list(node):
    """Select node wrapper for current node.

    Node type is list

    """
    if node:
        func = node[0]
        default = List if func.isflat else FirstBraceAlignList
        return NODES.get(func, default)(node)
    return List(node)
