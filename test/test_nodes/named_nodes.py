#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import parse


class TestNamedNodesPprint(unittest.TestCase):

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

    def test_if(self):
        strings = (
            ('(asdf (if (eq a z) a b))',
             '''\
(asdf
  (if (eq a z)
      a
    b))'''),

            ('(asdf (if (and (and a b) z) (asdf a (b c)) (asfd c d)))',
             '''\
(asdf
  (if (and (and a b)
           z)
      (asdf
        a
        (b c))
    (asfd c d)))'''),

            ('(asdf (if (and (and a (a b)) (or a ab)) (asdf a (b c)) (asfd c (k k))))',
             '''\
(asdf
  (if (and (and a
                (a b))
           (or a ab))
      (asdf
        a
        (b c))
    (asfd
      c
      (k k))))'''),
            ('(asdf (if ((a b) (a k) (a z)) a b))',
             '''\
(asdf
  (if ((a b)
       (a k)
       (a z))
      a
    b))'''),

        )
        self._test_parsed(strings)

    def test_defun(self):
        strings = (
            ('(defun x())',
             '''\
(defun x ())'''),

            ('(defun x (a b c) "Some docstring")',
             '''\
(defun x (a b c)
  "Some docstring")'''),

            ('(defun x (a b c) "Some docstring" (message "hello"))',
             '''\
(defun x (a b c)
  "Some docstring"
  (message "hello"))'''),
        )
        self._test_parsed(strings)

    def test_setf(self):
        strings = (
            ('(setf x y)',
             '''\
(setf x y)'''),

            ('(setf x y xx yy xxx yyy)',
             '''\
(setf x y
      xx yy
      xxx yyy)'''),

            ('(setf (a b) (c d) (aa bb) (cc dd) (aaa ccc) (ddd fff))',
             '''\
(setf (a b) (c d)
      (aa bb) (cc dd)
      (aaa ccc) (ddd fff))'''),

            ('(setf a b c d e)',
             '''\
(setf a b
      c d
      e)'''),
        )
        self._test_parsed(strings)

    def test_dolist(self):
        strings = (
            ('(asdf\n  (dolist (a b) (c d)))',
             '''\
(asdf
  (dolist (a b)
    (c d)))'''),

            ('(asdf\n  (dolist (a b) (hello) a 1 (+ 1 2 )))',
             '''\
(asdf
  (dolist (a b)
    (hello)
    a
    1
    (+ 1 2)))'''),
        )

        self._test_parsed(strings)
