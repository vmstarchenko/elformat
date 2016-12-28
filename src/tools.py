#! /usr/bin/env python3


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
