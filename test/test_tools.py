#! /usr/bin/env python3
# pylint: disable=C0111,C0103

import unittest
from src import abstractmethod, CallAbstractMethod


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
