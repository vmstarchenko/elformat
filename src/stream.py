#! /usr/bin/env python3


class Stream:
    """Stream."""

    def __init__(self, string):
        self._string = string
        self._size = len(string)
        self._state = 0

    def __repr__(self):
        return '[%s; %s:%s]' % (repr(self._string), self._state, self._size)

    def __bool__(self):
        return self._state < self._size

    __nonzero__ = __bool__

    def get(self, move=True):
        """Return character from stream or None if stream was finished.

        If move is True increase stream position

        """
        char = self._string[self._state] if self._size < self._state else None
        if move is True:
            self._state += 1
        return char

    def get_slice(self, start, stop=None):
        """Return slice of stream string from start to stop (without stop
        element).

        If stop is None

        """
        if not stop is None:
            return self._string[start:stop]
        return self._string[start:]

    def skip(self, characters={'\r', '\n', '\x0b', '\x0c', ' ', '\t'}.copy()):
        """Skip symbols from iterable object characters."""

        characters = set(characters)
        while self._state < self._size and self._string[self._state] in characters:
            self._state += 1

    def skipnot(self, characters={'\r', '\n', '\x0b', '\x0c', ' ', '\t'}.copy()):
        """Skip symbols that not in iterable object."""

        characters = set(characters)
        while (self._state < self._size and
               self._string[self._state] not in characters):
            self._state += 1

    def get_state(self):
        """Get current stream position."""
        return self._state

    def set_state(self, state):
        """Set state position.

        Set 0 if position less than 0 and set stream size if state
        grater than max stream position.

        """
        self._state = max(0, min(state, self._size))

    def change_state(self, value):
        """Move state position.

        Add value to state.

        """
        self._state = max(0, min(value + self._state, self._size))

    def get_size(self):
        """Return amount of characters left in stream."""
        return self._size - self._state

    def get_full_size(self):
        """Return strings of stream size."""
        return self._size
