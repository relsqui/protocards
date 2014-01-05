import unittest
import random

from pydeck import standard


class TestStandard(unittest.TestCase):
    def test_suit(self):
        suit = standard.Suit("FOO")
        self.assertEqual(suit.name, "FOO")
        self.assertEqual(suit.plural, "FOOs")
        self.assertEqual(suit.short, "f")

    def test_card_init(self):
        good_args = [(standard.ACE, standard.SPADE),
                     (standard.RANKS[12], standard.SUITS[3])]
        for args in good_args:
            card = standard.StandardCard(*args)
            self.assertEqual(card.rank, standard.ACE)
            self.assertEqual(card.suit, standard.SPADE)
            self.assertEqual(card.short, "As")
            self.assertEqual(card.name, "Ace of Spades")

    def test_card_equality(self):
        card_a = standard.StandardCard(standard.ACE, standard.SPADE)
        card_b = standard.StandardCard(standard.ACE, standard.SPADE)
        self.assertEqual(card_a, card_b)

    def test_card_inequality(self):
        cards = {
            "As": standard.StandardCard(standard.ACE, standard.SPADE),
            "Ah": standard.StandardCard(standard.ACE, standard.HEART),
            "2h": standard.StandardCard(standard.TWO, standard.HEART)
        }
        self.assertTrue(cards["Ah"] < cards["As"])
        self.assertTrue(cards["Ah"] <= cards["As"])
        self.assertNotEqual(cards["Ah"], cards["As"])
        self.assertTrue(cards["Ah"] > cards["2h"])
        self.assertTrue(cards["Ah"] >= cards["2h"])
        self.assertNotEqual(cards["Ah"], cards["2h"])

    def test_hand_str(self):
        deck = standard.make_deck()
        self.assertEqual(str(deck),
                         "AKQJT98765432s AKQJT98765432h "
                         "AKQJT98765432d AKQJT98765432c") 

    def test_hand_by_suit(self):
        spades = standard.make_deck().by_suit(standard.SPADE)
        self.assertEqual(str(spades), "AKQJT98765432s")

    def test_hand_by_rank(self):
        aces = standard.make_deck().by_rank(standard.ACE)
        self.assertEqual(str(aces), "As Ah Ad Ac")


    def test_make_deck(self):
        hand = standard.StandardHand()
        for suit in standard.SUITS:
            for rank in standard.RANKS:
                hand.append(standard.StandardCard(rank, suit))
        deck = standard.make_deck()
        self.assertEqual(deck, hand)

    def test_make_deck_shuffle(self):
        random.seed(0)
        unshuffled = standard.make_deck(shuffle=False)
        shuffled = standard.make_deck(shuffle=True)
        self.assertNotEqual(unshuffled, shuffled)
