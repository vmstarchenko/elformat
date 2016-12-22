#! /usr/bin/env python3

import unittest
from src import parse, LispSyntaxError


class TestParse(unittest.TestCase):

    def test_valid_simple_input(self):
        string = '(setq a 1)'
        parsed = parse(string)
        self.assertEqual(parsed, [('setq', 'a', '1'), ])

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
