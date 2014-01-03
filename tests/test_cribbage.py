#!/usr/bin/python

import unittest

from pydeck import standard, cribbage


class TestCribbage(unittest.TestCase):
    def setUp(self):
        score = {"fifteens": 0, "pairs": 0, "runs": 0, "flush": 0,
                 "heels": 0, "nobs": 0}
        self.deck = standard.make_deck()
        self.dscore = score.copy()
        self.dscore.update(
                {"fifteens": 34528, "runs": 872415232, "pairs": 156})
        self.spades = self.deck.by_suit(standard.SPADE)
        self.sscore = score.copy()
        self.sscore.update(
                {"fifteens": 58, "runs": 13, "pairs": 0, "flush": 13})

    def test_value(self):
        values = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                  "8": 8, "9": 9, "T": 10, "J": 10, "Q": 10, "K": 10}
        for card in self.deck:
            self.assertEqual(cribbage.value(card), values[card.rank.short])

    def test_pairs(self):
        self.assertEqual(cribbage.score_pairs(self.deck),
                         self.dscore["pairs"])
        self.assertEqual(cribbage.score_pairs(self.spades),
                         self.sscore["pairs"])
        hand = self.deck.by_rank(standard.ACE)
        self.assertEqual(cribbage.score_pairs(hand), 12)
        hand.pop()
        self.assertEqual(cribbage.score_pairs(hand), 6)
        hand.pop()
        self.assertEqual(cribbage.score_pairs(hand), 2)
        hand.pop()
        self.assertEqual(cribbage.score_pairs(hand), 0)

    def test_fifteens(self):
        self.assertEqual(cribbage.score_fifteens(self.deck),
                         self.dscore["fifteens"])
        self.assertEqual(cribbage.score_fifteens(self.spades),
                         self.sscore["fifteens"])
        hand = self.deck.by_rank(standard.FIVE)
        discards = standard.StandardHand()
        self.assertEqual(cribbage.score_fifteens(hand), 8)
        discards.append(hand.pop())
        self.assertEqual(cribbage.score_fifteens(hand), 2)
        discards.append(hand.pop())
        self.assertEqual(cribbage.score_fifteens(hand), 0)
        hand += discards + self.deck.by_rank(standard.JACK)
        self.assertEqual(cribbage.score_fifteens(hand), 40)

    def test_runs(self):
        self.assertEqual(cribbage.score_runs(self.deck),
                         self.dscore["runs"])
        self.assertEqual(cribbage.score_runs(self.spades),
                         self.sscore["runs"])
        hand = self.deck.by_rank(standard.ACE)
        self.assertEqual(cribbage.score_runs(hand), 0)
        hand += self.deck.by_rank(standard.TWO)
        self.assertEqual(cribbage.score_runs(hand), 0)
        hand += self.deck.by_rank(standard.THREE)
        self.assertEqual(cribbage.score_runs(hand), 192)

    def test_flush(self):
        self.assertFalse(cribbage.check_flush(self.deck))
        self.assertTrue(cribbage.check_flush(self.spades))
        self.assertFalse(cribbage.check_flush(self.deck.by_rank(standard.ACE)))

    def test_score(self):
        self.assertEqual(cribbage.score_hand(self.deck), self.dscore)
        self.assertEqual(cribbage.score_hand(self.spades), self.sscore)

    def test_score_crib_noturn(self):
        hand = self.spades.deal(4)
        score = cribbage.score_hand(hand, crib=False)
        self.assertEqual(score["flush"], 4)
        score = cribbage.score_hand(hand, crib=True)
        self.assertEqual(score["flush"], 4)

    def test_score_crib_turn(self):
        hand = self.spades.deal(4)
        turned = self.deck.by_suit(standard.HEART).pop()
        score = cribbage.score_hand(hand, turned=turned, crib=False)
        self.assertEqual(score["flush"], 4)
        score = cribbage.score_hand(hand, turned=turned, crib=True)
        self.assertEqual(score["flush"], 0)
        turned = self.spades.pop()
        score = cribbage.score_hand(hand, turned=turned, crib=False)
        self.assertEqual(score["flush"], 5)
        score = cribbage.score_hand(hand, turned=turned, crib=True)
        self.assertEqual(score["flush"], 5)

    def test_score_dealer_noturn(self):
        self.assertEqual(cribbage.score_hand(self.deck, dealer=True),
                         self.dscore)
        self.assertEqual(cribbage.score_hand(self.spades, dealer=True),
                         self.sscore)

    def test_score_heels(self):
        hand = self.deck.by_rank(standard.FIVE)
        turned = self.deck.by_rank(standard.JACK).pop()
        score = cribbage.score_hand(hand, turned=turned, dealer=False)
        self.assertEqual(score["heels"], 0)
        score = cribbage.score_hand(hand, turned=turned, dealer=True)
        self.assertEqual(score["heels"], 2)

    def test_score_nobs(self):
        hand = self.deck.by_rank(standard.JACK)
        turned = self.deck.by_rank(standard.FIVE).pop()
        for d in [True, False]:
            score = cribbage.score_hand(hand, turned=turned, dealer=d)
            self.assertEqual(score["nobs"], 1)
