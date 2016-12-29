#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import abstractmethod, CallAbstractMethod, curry, CurryingError


class TestTools(unittest.TestCase):

    def test_call_abstract_method(self):
        class A:

            @abstractmethod
            def a(self):
                pass

        a = A()
        self.assertRaises(CallAbstractMethod, a.a)

    def test_call_reloaded_abstract_method(self):
        class A:

            @abstractmethod
            def a(self):
                pass

        class B:

            def a(self):
                return True

        b = B()
        self.assertEqual(b.a(), True)

    def test_currying(self):
        def func(a, b, c):
            return a + b + c
        cfunc = curry(func, 3)

        self.assertEqual(cfunc(1, 2, 3), 6)
        self.assertEqual(cfunc(1, 2)(3), 6)
        self.assertEqual(cfunc(1)(2, 3), 6)
        self.assertEqual(cfunc(1)(2)(3), 6)
        self.assertRaises(CurryingError, cfunc(1, 2), 3, 4)
