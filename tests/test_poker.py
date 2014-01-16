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

    def test_best_sets(self):
        best_sets = {
            "deck": [self.hands["aces"]],
            "spades": [],
            "mixed": [std.StandardHand([std.StandardCard(std.ACE, std.SPADE),
                                        std.StandardCard(std.ACE, std.CLUB)])],
            "aces": [self.hands["aces"]],
            "empty": [],
        }
        for hand in self.hands:
            self.assertEqual(poker.best_sets(self.hands[hand]), best_sets[hand])

    def test_best_flushes(self):
        best_flushes = {
            "deck": std.find_flushes(self.hands["deck"]),
            "spades": [self.hands["spades"]],
            "mixed": [self.hands["spades"]],
            "aces": [std.StandardHand([a]) for a in self.hands["aces"]],
            "empty": [],
        }
        for hand in self.hands:
            print hand
            self.assertEqual(poker.best_flushes(self.hands[hand]),
                             best_flushes[hand])
        low = self.hands["spades"][:5]
        high = self.hands["deck"].by_suit(std.CLUB)[-5:]
        self.assertEqual(poker.best_flushes(low + high), [high])
