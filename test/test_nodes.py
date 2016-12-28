#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import parse


class TestPprint(unittest.TestCase):

    def _test_parsed(self, strings):
        for string, answer in strings:
            with self.subTest(i=string):
                print(parse(string))
                parsed = parse(string)[0]
                self.assertEqual(parsed.pprint(), answer)

    def test_simple_pprint_cases(self):
        strings = (
            (' ( setq    a  1 )',
             '(setq a 1)'),
            (' ( setq    hello  "str" )',
             '(setq hello "str")'),
        )
        self._test_parsed(strings)

    def test_let(self):
        print('\n\n\n')
        strings = (
            (' ( setq    (let ())  1 )',
             '(setq (let ()) 1)'),
            ('(setq (let* ()) 1)',
             '(setq (let* ()) 1)'),
            ('(setq (let* ((a b)) 1))',
             '(setq (let* ((a b)) 1))'),
        )
        self._test_parsed(strings)
