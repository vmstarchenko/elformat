#! /usr/bin/env python3

from .stream import Stream

NOT_ATOM_CHARACTERS = frozenset((
    '\r', '\n', '\x0b', '\x0c', ' ', '\t', '(', ')', '[', ']',
    "'", ',', '`', '#', ',', '"'))


class LispStream(Stream):
    """Extends Stream class, add functions for reading Lisp functions."""

    def read_string(self):
        """Try to read string from stream.

        Return tuple (begin, end) if string was read successfully ans
        set stream state to end string position. If first or last string
        char is not a string literal brace return None and doesn't
        change stream state.

        """
        if self._state >= self._size or self._string[self._state] != '"':  # check first char
            return None

        start_state = self._state
        self._state += 1

        while (self._state < self._size and
               self._string[self._state] != '"'):
            if self._string[self._state] == '\\':
                self._state += 1
            self._state += 1

        if self._state >= self._size or self._string[self._state] != '"':
            self.set_state(start_state)
            return None

        self._state += 1
        return (start_state, self._state)

    def read_atom(self):
        """Try to read atom from stream.

        Return tuple (begin, end) if atom was read successfully and set
        stream state to end atom position. If can't read atom (first
        character is not valid) return None

        """
        print(1)
        if self._state >= self._size or \
           self._string[self._state] in NOT_ATOM_CHARACTERS:  # check first char
            return None

        print(2)
        start_state = self._state

        while (self._state < self._size and
               not self._string[self._state] in NOT_ATOM_CHARACTERS):
            if self._string[self._state] == '\\':
                self._state += 1
            self._state += 1

        print(3, self._state, self._size, len(self._string))
        if self._state > self._size:
            self.set_state(start_state)
            return None

        return (start_state, self._state)
