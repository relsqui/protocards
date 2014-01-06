import unittest
import random

from pydeck import standard as std


class TestStandard(unittest.TestCase):
    def setUp(self):
        self.deck = std.make_deck()
        self.spades = self.deck.by_suit(std.SPADE)
        self.aces = self.deck.by_rank(std.ACE)
        self.mixed = self.spades + self.deck.by_suit(std.CLUB).deal(12)

    def test_suit(self):
        suit = std.Suit("FOO")
        self.assertEqual(suit.name, "FOO")
        self.assertEqual(suit.plural, "FOOs")
        self.assertEqual(suit.short, "f")

    def test_card_init(self):
        arg_pairs = [(std.ACE, std.SPADE), (std.RANKS[12], std.SUITS[3])]
        for args in arg_pairs:
            card = std.StandardCard(*args)
            self.assertEqual(card.rank, std.ACE)
            self.assertEqual(card.suit, std.SPADE)
            self.assertEqual(card.short, "As")
            self.assertEqual(card.name, "Ace of Spades")

    def test_card_equality(self):
        card_a = std.StandardCard(std.ACE, std.SPADE)
        card_b = std.StandardCard(std.ACE, std.SPADE)
        self.assertEqual(card_a, card_b)

    def test_card_inequality(self):
        cards = {
            "As": std.StandardCard(std.ACE, std.SPADE),
            "Ah": std.StandardCard(std.ACE, std.HEART),
            "2h": std.StandardCard(std.TWO, std.HEART)
        }
        self.assertTrue(cards["Ah"] < cards["As"])
        self.assertTrue(cards["Ah"] <= cards["As"])
        self.assertNotEqual(cards["Ah"], cards["As"])
        self.assertTrue(cards["Ah"] > cards["2h"])
        self.assertTrue(cards["Ah"] >= cards["2h"])
        self.assertNotEqual(cards["Ah"], cards["2h"])

    def test_hand_str(self):
        self.assertEqual(str(self.deck),
                         "AKQJT98765432s AKQJT98765432h "
                         "AKQJT98765432d AKQJT98765432c")

    def test_hand_by_suit(self):
        spades = std.make_deck().by_suit(std.SPADE)
        self.assertEqual(str(spades), "AKQJT98765432s")

    def test_hand_by_rank(self):
        self.assertEqual(str(self.aces), "As Ah Ad Ac")

    def test_make_deck(self):
        hand = std.StandardHand()
        for suit in std.SUITS:
            for rank in std.RANKS:
                hand.append(std.StandardCard(rank, suit))
        self.assertEqual(hand, std.make_deck())

    def test_make_deck_shuffle(self):
        random.seed(0)
        unshuffled = std.make_deck(shuffle=False)
        shuffled = std.make_deck(shuffle=True)
        self.assertNotEqual(unshuffled, shuffled)

    def test_pairs(self):
        self.assertEqual(len(std.find_pairs(self.deck)), 78)
        self.assertEqual(len(std.find_pairs(self.spades)), 0)
        self.assertEqual(len(std.find_pairs(self.mixed)), 12)
        self.assertEqual(len(std.find_pairs(self.aces)), 6)
        self.assertEqual(len(std.find_pairs(std.StandardHand())), 0)

    def test_flushes(self):
        by_suits = [tuple(self.deck.by_suit(s)) for s in std.SUITS]
        ace_lists = [(a,) for a in self.aces]
        self.assertEqual(std.find_flushes(self.deck), by_suits)
        self.assertEqual(std.find_flushes(self.spades), [tuple(self.spades)])
        self.assertEqual(std.find_flushes(self.mixed), [tuple(self.spades)])
        self.assertEqual(std.find_flushes(self.aces), ace_lists)
        self.assertEqual(std.find_flushes(std.StandardHand()), [])
