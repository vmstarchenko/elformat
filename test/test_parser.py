#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import parse, LispSyntaxError


class TestParse(unittest.TestCase):

    def _test_parsed(self, strings):
        for string, answer in strings:
            with self.subTest(i=string):
                parsed = parse(string)
                self.assertEqual(parsed, answer)

    def test_valid_simple_input(self):
        strings = (('(setq a 1)',
                    [('setq', 'a', '1'), ]),
                   ('(setq () 1)',
                    [('setq', (), '1'), ]),
                   ('(setq (let* ((a b)) 1))',
                    [('setq', ('let*', (('a', 'b'),), '1'),), ]),)
        self._test_parsed(strings)

    def test_valid_string_input(self):
        strings = ['(setq a "1")', '""', '(setq x "(hello)")']
        answers = [[('setq', 'a', '"1"'), ],
                   ['""', ],
                   [('setq', 'x', '"(hello)"'), ], ]
        for string, answer in zip(strings, answers):
            with self.subTest(i=string):
                parsed = parse(string)
                self.assertEqual(parsed, answer)

    def test_not_valid_string_input(self):
        strings = ['(setq a "1)', '"', r'(setq a "" "1\"']
        for string in strings:
            with self.subTest(i=string):
                self.assertRaises(LispSyntaxError, parse, string)

    def test_unclosed_brace(self):
        string = '(setq a 1'
        self.assertRaises(LispSyntaxError, parse, string)

    def test_extra_brace(self):
        string = '(setq a 1))'
        self.assertRaises(LispSyntaxError, parse, string)
