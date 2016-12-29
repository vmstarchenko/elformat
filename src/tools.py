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


class CurryingError(BaseException):
    """Bind extra arguments."""
    pass


class curry:
    """Create wrapped function that calles after binding correct amount of
    arguments.

    If bind more arguments raise CurryingError.

    """

    def __init__(self, func, args_number=2):
        """args_number: amount of expected arguments."""
        self.func = func
        self.args_number = args_number
        self.args = []

    def __call__(self, *args, **kargs):
        args_number = len(self.args) + len(args)
        if args_number == self.args_number:
            return self.func(*(self.args + list(args)))
        elif args_number < self.args_number:
            newfunc = curry(self.func, self.args_number)
            newfunc.args = self.args.copy() + list(args)
            return newfunc
        raise CurryingError('bound extra arguments')
