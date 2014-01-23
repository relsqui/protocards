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

    def test_longer_stronger(self):
        clubs = self.hands["deck"].by_suit(std.CLUB)
        self.assertTrue(poker.LongerStronger(self.hands["spades"]) <
                        poker.LongerStronger(self.hands["deck"]))
        self.assertFalse(poker.LongerStronger(self.hands["spades"]) <
                         poker.LongerStronger(clubs))
        self.assertTrue(poker.LongerStronger(self.hands["empty"]) ==
                        poker.LongerStronger(std.StandardHand()))
        self.assertFalse(poker.LongerStronger(self.hands["mixed"]) ==
                         poker.LongerStronger(std.StandardHand()))

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
            self.assertEqual(poker.best_sets(self.hands[hand]),
                             best_sets[hand])

    def test_best_sets_short(self):
        best_sets = {
            "deck": [self.hands["aces"]],
            "spades": [],
            "mixed": [],
            "aces": [self.hands["aces"]],
            "empty": [],
        }
        for hand in self.hands:
            self.assertEqual(poker.best_sets(self.hands[hand], length=4),
                             best_sets[hand])

    def test_best_sets_long(self):
        best_sets = {
            "deck": [],
            "spades": [],
            "mixed": [std.StandardHand([std.StandardCard(std.ACE, std.SPADE),
                                        std.StandardCard(std.ACE, std.CLUB)])],
            "aces": [],
            "empty": [],
        }
        for hand in self.hands:
            self.assertEqual(poker.best_sets(self.hands[hand], length=2),
                             best_sets[hand])

    def test_best_flushes(self):
        best_flushes = {
            "deck": std.find_flushes(self.hands["deck"]),
            "spades": [self.hands["spades"]],
            "mixed": [self.hands["spades"]],
            "aces": [],
            "empty": [],
        }
        for hand in self.hands:
            self.assertEqual(poker.best_flushes(self.hands[hand]),
                             best_flushes[hand])
        low = self.hands["spades"][:5]
        high = self.hands["deck"].by_suit(std.CLUB)[-5:]
        self.assertEqual(poker.best_flushes(low + high), [high])

    def test_best_straights(self):
        best_straights = {
            "spades": [self.hands["spades"]],
            "aces": [],
            "empty": [],
        }
        for hand in best_straights:
            self.assertEqual(poker.best_straights(self.hands[hand]),
                             best_straights[hand])
        mixed_straights = poker.best_straights(self.hands["mixed"])
        self.assertEqual(len(mixed_straights), 2 ** 12)

    def test_straight_flushes(self):
        straight_flushes = {
            "deck": std.find_flushes(self.hands["deck"]),
            "spades": [self.hands["spades"]],
            "mixed": [self.hands["mixed"].by_suit(std.CLUB),
                      self.hands["spades"]],
            "aces": [],
            "empty": [],
        }
        for hand in straight_flushes:
            self.assertEqual(poker.find_straight_flushes(self.hands[hand]),
                             straight_flushes[hand])

    def test_full_houses(self):
        def count_fh(hand):
            return len(poker.find_full_houses(hand))

        twos = self.hands["deck"].by_rank(std.TWO)
        threes = self.hands["deck"].by_rank(std.THREE)
        fours = self.hands["deck"].by_rank(std.FOUR)
        hand = twos + threes
        self.assertEqual(count_fh(hand), 2)
        hand += fours
        self.assertEqual(count_fh(hand), 6)

    def test_best_full_houses(self):
        def fh_ranks(hand):
            triple, double = poker.split_full_house(hand)
            return triple[0].rank, double[0].rank

        twos = self.hands["deck"].by_rank(std.TWO)
        threes = self.hands["deck"].by_rank(std.THREE)
        fours = self.hands["deck"].by_rank(std.FOUR)

        hand = twos + threes
        best = poker.best_full_houses(hand)
        self.assertEqual(len(best), 1)
        best_fh = best[0]
        self.assertEqual(fh_ranks(best[0]), (std.THREE, std.TWO))

        hand += fours
        best = poker.best_full_houses(hand)
        self.assertEqual(len(best), 1)
        best_fh = best[0]
        self.assertEqual(fh_ranks(best[0]), (std.FOUR, std.THREE))

    def test_multi_best_full_houses(self):
        def fake_find_fh(hand):
            low = self.hands["deck"].by_rank(std.KING)[0:3] +\
                  self.hands["deck"].by_rank(std.QUEEN)[0:2]
            mid = self.hands["aces"][0:3] +\
                  self.hands["deck"].by_rank(std.QUEEN)[0:2]
            high = self.hands["aces"][0:3] +\
                   self.hands["deck"].by_rank(std.KING)[0:2]
            return [high, high, mid, low]

        real_find_fh = poker.find_full_houses
        poker.find_full_houses = fake_find_fh
        best = poker.best_full_houses(self.hands["empty"])
        self.assertEqual(len(best), 2)
        poker.find_full_houses = real_find_fh
