#! /usr/bin/env python3

"""Auxiliary tools for project."""

PYTHON_VERSION = 3 if hasattr(list, 'copy') else 2
DEBUG = True


class CallAbstractMethod(BaseException):
    """Call abstract method case."""
    pass


def abstractmethod(func):
    """Call function and raise CallAbstractMethod error."""
    def fwrapper(*args, **kargs):
        """func wrapper."""
        func(*args, **kargs)
        raise CallAbstractMethod
    return fwrapper


class CurryingError(BaseException):
    """Bind extra arguments."""
    pass
