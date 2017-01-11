#! /usr/bin/env python3


"""Stream specified for reading lisp syntax structures."""

from .stream import Stream

NOT_ATOM_CHARACTERS = frozenset((
    '\r', '\n', '\x0b', '\x0c', ' ', '\t', '(', ')', '[', ']',
    "'", ',', '`', '#', ',', '"'))


class LispSyntaxError(ValueError):
    """Error for not valid lisp programms."""
    pass


class LispStream(Stream):
    """Extends Stream class, add functions for reading Lisp functions."""

    def read_string(self):
        """Try to read string from stream.

        Return string if string was read successfully and set stream
        state to end string position. If first or last string char is
        not a string literal brace return None and doesn't change stream
        state.

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
        return self._string[start_state:self._state]

    def read_atom(self):
        """Try to read atom from stream.

        Return atom if atom was read successfully and set stream state
        to end atom position. If can't read atom (first character is not
        valid) return None

        """
        if self._state >= self._size or \
           self._string[self._state] in NOT_ATOM_CHARACTERS:  # check first char
            return None

        start_state = self._state

        while (self._state < self._size and
               not self._string[self._state] in NOT_ATOM_CHARACTERS):
            if self._string[self._state] == '\\':
                self._state += 1
            self._state += 1

        if self._state > self._size:
            self.set_state(start_state)
            return None

        return self._string[start_state:self._state]

    def read_comment(self):
        """Try to comment atom from stream.

        Return comment if comment was read successfully and set stream
        state to end comment position. If can't read comment (first
        character is not valid) return None

        """
        if self._state >= self._size or \
           self._string[self._state] != ';':  # check first char
            return None

        start_state = self._state

        while (self._state < self._size and
               self._string[self._state] != '\n'):
            self._state += 1

        if self._state > self._size:
            self.set_state(start_state)
            return None

        return self._string[start_state:self._state]
