#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import parse


class TestBaseNodesPprint(unittest.TestCase):

    def _test_parsed(self, strings, DEBUG=False):
        for string, answer in strings:
            with self.subTest(i=string):
                parsed = parse(string)
                pprint = parsed.pprint()
                self.assertEqual(
                    pprint,
                    answer,
                    '\nResult:\n%s\nCorrectAnswer:\n%s\n' % (pprint, answer))
                if DEBUG or pprint != answer:
                    print('\nTest', repr(string))
                    print('ans:\n', answer, sep='')
                    print('pprint:\n', pprint, sep='')
                    print()

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

            ('(a () b c)',
             '''\
(a () b c)'''),
        )
        self._test_parsed(strings)

    def test_function_align(self):
        strings = (
            ('(a (and x y z))',
             '''\
(a
  (and x y z))'''),

            ('(a (and (or a b 2 (3 c)) (or (c d) (and x y)) z))',
             '''\
(a
  (and (or a
           b
           2
           (3 c))
       (or (c d)
           (and x y))
       z))'''),
        )
        self._test_parsed(strings)

    def test_first_brace_align(self):
        strings = (
            ('((k x y z))',
             '''\
((k x y z))'''),

            ('((k x y z) (a b))',
             '''\
((k x y z)
 (a b))'''),

        )
        self._test_parsed(strings)

    def test_comments_levels(self):
        strings = (
            ('(hello ; simple comment\n me)',
             '''\
(hello ; simple comment
  me)'''),

            ('(hello ;; simple comment\n me)',
             '''\
(hello
  ;; simple comment
  me)'''),

            ('(hello ;;; simple comment\n me)',
             '''\
(hello
;;; Simple comment
  me)'''),

            ('(hello ;;;; simple comment\n me)',
             '''\
(hello
;;;; Simple comment
  me)'''),)

        self._test_parsed(strings)

    def test_simple_programm(self):
        strings = (
            ('(hello me)',
             '''\
(hello me)'''),

            ('(hello me)(hello)',
             '''\
(hello me)
(hello)'''), )
        self._test_parsed(strings)

    @unittest.skip('TODO: write Programm class for more difficult tests')
    def test_programm(self):
        strings = (
            (';;;first message\n(let ((hello ;; for x\n a) ; smth\n b (c 1)) (body);; message\n (mess))',
             '''\
;;; first message

(let ((hello
       ;; for x
       a) ; smth
      b
      (c 1))
  (body)
  ;; message
  (mess))'''),)

        self._test_parsed(strings, True)
