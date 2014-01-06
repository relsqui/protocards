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
            self.assertEqual(str(card), "Ace of Spades")
            self.assertEqual(repr(card), "<StandardCard:As>")

    def test_card_equality(self):
        ace1 = std.StandardCard(std.ACE, std.SPADE)
        ace2 = std.StandardCard(std.ACE, std.SPADE)
        two = std.StandardCard(std.TWO, std.SPADE)
        self.assertTrue(ace1 == ace2)
        self.assertFalse(ace1 != ace2)
        self.assertTrue(ace1 != two)
        self.assertFalse(ace1 == two)

    def test_hand_str(self):
        self.assertEqual(str(self.deck), "AKQJT98765432s AKQJT98765432h "
                                         "AKQJT98765432d AKQJT98765432c")
        ace = std.StandardCard(std.ACE, std.SPADE)
        two = std.StandardCard(std.TWO, std.SPADE)
        hand = std.StandardHand([ace, two])
        self.assertEqual(repr(hand), "<StandardHand:As,2s>")

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
        self.assertNotEqual(list(unshuffled), list(shuffled))
