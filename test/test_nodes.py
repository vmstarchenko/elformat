#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import parse

class TestPprint(unittest.TestCase):

    def _test_parsed(self, strings):
        for string, answer in strings:
            with self.subTest(i=string):
                parsed = parse(string)[0]
                pprint = parsed.pprint()
                self.assertEqual(
                    pprint,
                    answer,
                    '\nResult:\n%s\nCorrectAnswer:\n%s\n' %(pprint, answer))

    def test_simple_pprint_cases(self):
        strings = (
            (' ( asdf    a  1 )',
             '''(asdf a 1)'''),

            (' ( asdf    hello  "str" )',
             '''(asdf hello "str")'''),

            ('(asdf (str b))',
             '''\
(asdf
  (str b))'''),

            ('(a 1 (+ 1 2))',
             '''\
(a
  1
  (+ 1 2))'''),
        )
        self._test_parsed(strings)

    def test_let(self):
        strings = (
            (' ( asdf    (let ())  1 1 )',
             '''\
(asdf
  (let ())
  1
  1)'''),

            ('(asdf\n  (let* ())\n1)',
             '''\
(asdf
  (let* ())
  1)\
'''),

            ('(asdf\n  (let* ((a b) (c d))))',
             '''\
(asdf
  (let* ((a b)
         (c d))))'''),

            ('(asdf\n  (let* ((a b) (c d)) (hello) a 1 (+ 1 2 )))',
             '''\
(asdf
  (let* ((a b)
         (c d))
    (hello)
    a
    1
    (+ 1 2)))'''),
        )

        self._test_parsed(strings)

    def test_function_align(self):
        strings = (
            ('(a (and x y z))',
             '''\
(a
  (and x y z))'''),

            ('(a (and (or a b 2 (3 c)) (or c (and x y)) z))',
             '''\
(a
  (and (or a
           b
           2
           (3 c))
       (or c
           (and x y))
       z))'''),
        )
        self._test_parsed(strings)
