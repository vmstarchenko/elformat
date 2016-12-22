#! /usr/bin/env python3

import unittest
from src import Stream


class TestStream(unittest.TestCase):

    def setUp(self):
        self.strings = ['hello', '']

    def test_init_stream_with_different_input_strings(self):
        for string in self.strings:
            with self.subTest(i=string):
                stream = Stream(string)
                self.assertEqual(0, stream.get_state())

    def test_bool(self):
        true_stream = Stream('hello')
        self.assertTrue(bool(true_stream))
        false_stream = Stream('')
        self.assertFalse(bool(false_stream))

    def test_get_state_and_set_state(self):
        for string in self.strings:
            with self.subTest(i=string):
                str_len = len(string)
                stream = Stream(string)
                self.assertEqual(stream.get_state(), 0)
                stream.set_state(str_len + 10)
                self.assertEqual(stream.get_state(), str_len)
                stream.set_state(-3)
                self.assertEqual(stream.get_state(), 0)

    def test_get(self):
        for string in self.strings:
            with self.subTest(i=string):
                stream = Stream(string)
                i = 0
                string_size = len(string)
                while stream.get(False):
                    self.assertEqual(stream.get(), string[i])
                    # if move in infinity cycle
                    print(i, string_size)
                    self.assertLess(i, string_size)
                    i += 1

    def test_get_slice(self):
        string = 'asdf dsafas wejkfjal'
        stream = Stream(string)
        self.assertEqual(stream.get_slice(0), string)
        stream.skipnot()
        stream.skip()
        start = stream.get_state()
        stream.skipnot()
        stop = stream.get_state()
        self.assertEqual(stream.get_slice(start, stop), string.split(' ')[1])

    def test_skip_on_empty_string(self):
        stream = Stream('')
        stream.skip()
        self.assertEqual(stream.get_state(), 0)

    def test_skip_full_string(self):
        string = 'aaaaa'
        stream = Stream(string)
        stream.skip('a')
        self.assertFalse(bool(stream))

    def test_skip_word(self):
        string = 'asdf asdf'
        stream = Stream(string)
        stream.skip('qwertyuiopasdfghjklzxcvbnm')
        self.assertEqual(stream.get_state(), 4)

    def test_skipnot_on_empty_string(self):
        stream = Stream('')
        stream.skipnot()
        self.assertEqual(stream.get_state(), 0)

    def test_skipnot_full_string(self):
        string = 'aaaaa'
        stream = Stream(string)
        stream.skipnot('a')
        self.assertEqual(stream.get_state(), 0)

    def test_skipnot_word(self):
        string = 'asdf asdf'
        stream = Stream(string)
        stream.skipnot()
        self.assertEqual(stream.get_state(), 4)

    def test_get_size(self):
        for string in self.strings:
            with self.subTest(i=string):
                stream = Stream(string)
                for i in range(len(string), -1, -1):
                    self.assertEqual(stream.get_size(), i)
                    stream.get()

    def test_get_full_size(self):
        for string in self.strings:
            with self.subTest(i=string):
                self.assertEqual(Stream(string).get_full_size(), len(string))
