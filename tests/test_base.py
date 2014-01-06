import unittest
import random

from pydeck import base


class TestBase(unittest.TestCase):
    def test_property_attrs(self):
        prop = base.CardProperty("bar")
        self.assertEqual(prop.name, "bar")
        self.assertEqual(prop.plural, "bars")
        self.assertEqual(prop.short, "b")

    def test_shuffle(self):
        data = [1, 2, 3, 4, 5]
        hand = base.Hand(data)
        self.assertEqual(hand.data, data)
        random.seed(0)
        hand.shuffle()
        self.assertNotEqual(hand.data, data)

    def test_deal(self):
        hand = base.Hand([1, 2, 3, 4, 5])
        book = hand.deal(3)
        self.assertEqual(hand.data, [1, 2])
        self.assertEqual(book.data, [3, 4, 5])

    def test_deal_toomany(self):
        hand = base.Hand([1, 2, 3, 4, 5])
        self.assertRaises(IndexError, hand.deal, 10)


class TestEqualityMixin(unittest.TestCase):
    def setUp(self):
        class Foo(base.EqualityMixin):
            pass

        class Bar(base.EqualityMixin):
            pass
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
