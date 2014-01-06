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

    def test_hand_str(self):
        self.assertEqual(str(self.deck), "AKQJT98765432s AKQJT98765432h "
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
        self.assertNotEqual(list(unshuffled), list(shuffled))

    def test_pairs(self):
        self.assertEqual(len(std.find_pairs(self.deck)), 78)
        self.assertEqual(len(std.find_pairs(self.spades)), 0)
        self.assertEqual(len(std.find_pairs(self.mixed)), 12)
        self.assertEqual(len(std.find_pairs(self.aces)), 6)
        self.assertEqual(len(std.find_pairs(std.StandardHand())), 0)

    def test_flushes(self):
        ace_spades = std.StandardHand([std.StandardCard(std.ACE, std.SPADE)])
        empty_hand = std.StandardHand()
        self.assertEqual(std.best_flush(self.deck), self.spades)
        self.assertEqual(std.best_flush(self.spades), self.spades)
        self.assertEqual(std.best_flush(self.mixed), self.spades)
        self.assertEqual(std.best_flush(self.aces), ace_spades)
        self.assertEqual(std.best_flush(empty_hand), empty_hand)
        low = self.spades[:5]
        high = self.deck.by_suit(std.CLUB)[-5:]
        self.assertEqual(std.best_flush(low + high), high)
