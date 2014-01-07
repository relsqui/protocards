import unittest

from pydeck import poker, standard as std


class TestStandard(unittest.TestCase):
    def setUp(self):
        self.deck = std.make_deck()
        self.spades = self.deck.by_suit(std.SPADE)
        self.mixed = self.spades + self.deck.by_suit(std.CLUB).deal(12)
        self.aces = self.deck.by_rank(std.ACE)

    def test_sets(self):
        hands = [self.deck, self.spades, self.mixed, self.aces,
                 std.StandardHand()]
        sets = [[self.deck.by_rank(r) for r in std.RANKS],
                [],
                [std.StandardHand([std.StandardCard(r, std.SPADE),
                                  std.StandardCard(r, std.CLUB)])
                                 for r in std.RANKS[1:]],
                [self.aces],
                []]
        for i in range(len(hands)):
            self.assertEqual(poker.find_sets(hands[i]), sets[i])

    def test_best_set(self):
        hands = [self.deck, self.spades, self.mixed, self.aces,
                 std.StandardHand()]
        sets = [self.aces,
                std.StandardHand(),
                std.StandardHand([std.StandardCard(std.ACE, std.SPADE),
                                  std.StandardCard(std.ACE, std.CLUB)]),
                self.aces,
                std.StandardHand()]
        for i in range(len(hands)):
            print hands[i]
            self.assertEqual(poker.best_set(hands[i]), sets[i])

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
