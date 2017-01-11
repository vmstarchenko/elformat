#! /usr/bin/env python3
# pylint: disable=C0111,C0103


import unittest
from src import LispStream


class TestLispStream(unittest.TestCase):

    def test_read_string_on_empty_string(self):
        stream = LispStream('"" hello it is a test for empty string')
        string = stream.read_string()
        self.assertEqual(string, '""')

    def test_read_string_on_unclosed_string(self):
        stream = LispStream('" hello ')
        string = stream.read_string()
        self.assertIsNone(string, None)
        self.assertEqual(stream.get_state(), 0)
        stream = LispStream(r'" hello \"')
        string = stream.read_string()
        self.assertIsNone(string, None)
        self.assertEqual(stream.get_state(), 0)

    def test_read_string_on_atom(self):
        stream = LispStream('hello it is a test for empty string')
        string = stream.read_string()
        self.assertIsNone(string, None)
        self.assertEqual(stream.get_state(), 0)

    def test_read_string_on_string_with_escaped_symbols(self):
        stream = LispStream(r'"\\hello it \"is" a test for empty string')
        string = stream.read_string()
        self.assertEqual(string, r'"\\hello it \"is"')
        stream = LispStream(r'"\"" a')
        string = stream.read_string()
        self.assertEqual(string, r'"\""')

    def test_read_atom_on_empty_string(self):
        stream = LispStream('')
        string = stream.read_atom()
        self.assertIsNone(string)
        self.assertEqual(stream.get_state(), 0)

    def test_read_atom_on_not_valid_string(self):
        stream = LispStream('kek\\')
        string = stream.read_atom()
        self.assertIsNone(string)
        self.assertEqual(stream.get_state(), 0)

    def test_read_atom_on_valid_atom(self):
        strings = [
            'one)', "one\'", 'one(', 'one,', 'one ', 'one`', 'one"', 'one[',
            'one]', 'one#', 'one\t']
        for string in strings:
            with self.subTest(i=string):
                stream = LispStream(string)
                string = stream.read_atom()
                self.assertEqual(string, 'one')
                self.assertEqual(stream.get_state(), 3)

    def test_read_comment(self):
        strings = [(
            ';; hello\nworld',
            ';; hello'),]
        for string, ans in strings:
            with self.subTest(i=string):
                stream = LispStream(string)
                string = stream.read_comment()
                self.assertEqual(string, ans)
