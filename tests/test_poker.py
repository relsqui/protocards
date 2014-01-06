import unittest

from pydeck import poker, standard as std


class TestStandard(unittest.TestCase):
    def setUp(self):
        self.deck = std.make_deck()
        self.spades = self.deck.by_suit(std.SPADE)
        self.aces = self.deck.by_rank(std.ACE)
        self.mixed = self.spades + self.deck.by_suit(std.CLUB).deal(12)

    def test_pairs(self):
        self.assertEqual(len(poker.find_pairs(self.deck)), 78)
        self.assertEqual(len(poker.find_pairs(self.spades)), 0)
        self.assertEqual(len(poker.find_pairs(self.mixed)), 12)
        self.assertEqual(len(poker.find_pairs(self.aces)), 6)
        self.assertEqual(len(poker.find_pairs(std.StandardHand())), 0)

    def test_flushes(self):
        ace_spades = std.StandardHand([std.StandardCard(std.ACE, std.SPADE)])
        empty_hand = std.StandardHand()
        self.assertEqual(poker.best_flush(self.deck), self.spades)
        self.assertEqual(poker.best_flush(self.spades), self.spades)
        self.assertEqual(poker.best_flush(self.mixed), self.spades)
        self.assertEqual(poker.best_flush(self.aces), ace_spades)
        self.assertEqual(poker.best_flush(empty_hand), empty_hand)
        low = self.spades[:5]
        high = self.deck.by_suit(std.CLUB)[-5:]
        self.assertEqual(poker.best_flush(low + high), high)
