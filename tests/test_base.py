#!/usr/bin/python

import unittest
import random

from pydeck import base


class TestBase(unittest.TestCase):
    def test_property_attrs(self):
        foo = base.CardProperty("bar")
        self.assertEqual(foo.name, "bar")
        self.assertEqual(foo.plural, "bars")
        self.assertEqual(foo.short, "b")

    def test_shuffle(self):
        data = [1, 2, 3, 4, 5]
        foo = base.Hand(data)
        self.assertEqual(foo.data, data)
        random.seed(0)
        foo.shuffle()
        self.assertNotEqual(foo.data, data)

    def test_deal(self):
        foo = base.Hand([1, 2, 3, 4 ,5])
        bar = foo.deal(3)
        self.assertEqual(foo.data, [4, 5])
        self.assertEqual(bar.data, [1, 2, 3])


class TestEqualityMixin(unittest.TestCase):
    def setUp(self):
        class Foo(base.EqualityMixin): pass
        class Bar(base.EqualityMixin): pass
        self.Foo = Foo
        self.Bar = Bar

    def test_same_class_same_attrs(self):
        a = self.Foo()
        b = self.Foo()
        a.use = "fruit"
        b.use = "fruit"
        self.assertEqual(a, b)

    def test_different_class_same_attrs(self):
        a = self.Foo()
        b = self.Bar()
        a.use = "fruit"
        b.use = "fruit"
        self.assertEqual(a, b)

    def test_same_class_different_attrs(self):
        a = self.Foo()
        b = self.Foo()
        a.name = "apple"
        b.name = "banana"
        self.assertNotEqual(a, b)

    def test_different_class_different_attrs(self):
        a = self.Foo
        b = self.Bar
        a.name = "apple"
        b.name = "banana"
        self.assertNotEqual(a, b)
