#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import parse


class TestPprint(unittest.TestCase):

    def _test_parsed(self, strings):
        for string, answer in strings:
            with self.subTest(i=string):
                parsed = parse(string)[0]
                print('pprint')
                print(parsed.pprint())
                print('ans')
                print(answer)
                self.assertEqual(parsed.pprint(), answer)

    def test_simple_pprint_cases(self):
        strings = (
            (' ( asdf    a  1 )',
             '(asdf a 1)'),
            (' ( asdf    hello  "str" )',
             '(asdf hello "str")'),
            ('(asdf (str b))',
             '(asdf\n  (str b))'),
            ('(a 1 (+ 1 2))',
             '(a\n  1\n  (+ 1 2))'),
        )
        self._test_parsed(strings)

    def test_let(self):
        print('\n\n\n')
        strings = (
            (' ( asdf    (let ())  1 1 )',
             '(asdf\n  (let ())\n  1\n  1)'),
            ('(asdf\n  (let* ())\n1)',
             '(asdf\n  (let* ())\n  1)'),
            ('(asdf\n  (let* ((a b) (c d))))',
             '(asdf\n  (let* ((a b)\n         (c d))))'),
            ('(asdf\n  (let* ((a b) (c d)) (hello) a 1 (+ 1 2 )))',
             '(asdf\n  (let* ((a b)\n         (c d))\n    (hello)\n    a\n    1\n    (+ 1 2)))'),
        )
        self._test_parsed(strings)
