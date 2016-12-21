#! /usr/bin/env python3


class Stream:
    """Stream."""

    def __init__(self, string):
        self.string = string
        self.size = len(string)
        self.state = 0

    def __bool__(self):
        return self.state < self.size

    __nonzero__ = __bool__

    def __repr__(self):
        return repr((self.string, self.state, self.size))

    def get(self, move=True):
        """Return character from stream or None if stream was finished.

        if move is True increase stream position

        """
        char = self.string[self.state] if self.size < self.state else None
        if move is True:
            self.state += 1
        return char

    def skip(self, characters={'\r', '\n', '\x0b', '\x0c', ' ', '\t'}.copy()):
        """Skip symbols from iterable object characters."""

        characters = set(characters)
        while self.state < self.size and self.string[self.state] in characters:
            self.state += 1

    def skipnot(self, characters={'\r', '\n', '\x0b', '\x0c', ' ', '\t'}.copy()):
        """Skip symbols that not in iterable object."""

        characters = set(characters)
        while self.state < self.size and self.string[self.state] not in characters:
            self.state += 1

    def get_state(self):
        """Get current stream position."""
        return self.state

    def set_state(self, state):
        """Set state position.

        Set 0 if position less than 0 and set stream size if state
        grater than max stream position

        """
        self.state = max(0, min(state, self.size))

    def get_size(self):
        return self.size
