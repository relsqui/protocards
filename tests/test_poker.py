import unittest

from pydeck import poker, standard as std


class TestStandard(unittest.TestCase):
    def setUp(self):
        deck = std.make_deck()
        spades = deck.by_suit(std.SPADE)
        self.hands = {
            "deck": deck,
            "spades": spades,
            "mixed": spades + deck.by_suit(std.CLUB).deal(12),
            "aces": deck.by_rank(std.ACE),
            "empty": std.StandardHand()
        }

    def test_sets(self):
        sets = {
            "deck": [self.hands["deck"].by_rank(r) for r in std.RANKS],
            "spades": [],
            "mixed": [std.StandardHand([std.StandardCard(r, std.SPADE),
                                        std.StandardCard(r, std.CLUB)])
                                       for r in std.RANKS[1:]],
            "aces": [self.hands["aces"]],
            "empty": []
        }
        for hand in self.hands:
            self.assertEqual(poker.find_sets(self.hands[hand]), sets[hand])

    def test_best_set(self):
        best_sets = {
            "deck": self.hands["aces"],
            "spades": std.StandardHand(),
            "mixed": std.StandardHand([std.StandardCard(std.ACE, std.SPADE),
                                       std.StandardCard(std.ACE, std.CLUB)]),
            "aces": self.hands["aces"],
            "empty": self.hands["empty"]
        }
        for hand in self.hands:
            self.assertEqual(poker.best_set(self.hands[hand]), best_sets[hand])

    def test_flushes(self):
        flushes = {
            "deck": [self.hands["deck"].by_suit(std.CLUB),
                     self.hands["deck"].by_suit(std.DIAMOND),
                     self.hands["deck"].by_suit(std.HEART),
                     self.hands["deck"].by_suit(std.SPADE)],
            "spades": [self.hands["spades"]],
            "mixed": [self.hands["deck"].by_suit(std.CLUB)[1:],
                      self.hands["deck"].by_suit(std.SPADE)],
            "aces": [std.StandardHand([c]) for c in self.hands["aces"]],
            "empty": []
        }
        for hand in self.hands:
            self.assertEqual(poker.find_flushes(self.hands[hand]),
                             flushes[hand])

    def test_best_flush(self):
        best_flushes = {
            "deck": self.hands["spades"],
            "spades": self.hands["spades"],
            "mixed": self.hands["spades"],
            "aces": std.StandardHand([std.StandardCard(std.ACE, std.SPADE)]),
            "empty": self.hands["empty"]
        }
        for hand in self.hands:
            self.assertEqual(poker.best_flush(self.hands[hand]),
                             best_flushes[hand])
        low = self.hands["spades"][:5]
        high = self.hands["deck"].by_suit(std.CLUB)[-5:]
        self.assertEqual(poker.best_flush(low + high), high)

    def test_straights(self):
        def count_straights(hand):
            return len(poker.find_straights(hand))

        hand = std.StandardHand(self.hands["spades"])
        self.assertEqual(count_straights(hand), 1)
        hand.append(std.StandardCard(std.ACE, std.CLUB))
        self.assertEqual(count_straights(hand), 2)
        hand.append(std.StandardCard(std.TWO, std.CLUB))
        self.assertEqual(count_straights(hand), 4)
        hand.append(std.StandardCard(std.THREE, std.CLUB))
        self.assertEqual(count_straights(hand), 8)
        hand.append(std.StandardCard(std.ACE, std.HEART))
        self.assertEqual(count_straights(hand), 12)
