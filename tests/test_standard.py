import unittest
import random

from pydeck import standard as std


class TestStandard(unittest.TestCase):
    def setUp(self):
        deck = std.make_deck()
        spades = deck.by_suit(std.SPADE)
        separate = std.StandardHand([spades[0],
                                    std.StandardCard(std.SEVEN, std.CLUB)])
        self.hands = {
            "deck": deck,
            "spades": spades,
            "mixed": spades + deck.by_suit(std.CLUB).deal(12),
            "aces": deck.by_rank(std.ACE),
            "empty": std.StandardHand(),
            "separate": separate,
        }

    def test_suit(self):
        suit = std.Suit("FOO")
        self.assertEqual(suit.name, "FOO")
        self.assertEqual(suit.plural, "FOOs")
        self.assertEqual(suit.short, "f")

    def test_suit_equality(self):
        self.assertEqual(std.CLUB, std.CLUB)
        self.assertTrue(std.CLUB < std.SPADE)
        self.assertNotEqual(std.CLUB, std.SPADE)

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
        self.assertEqual(str(self.hands["deck"]),
                         "AKQJT98765432s AKQJT98765432h "
                         "AKQJT98765432d AKQJT98765432c")
        ace = std.StandardCard(std.ACE, std.SPADE)
        two = std.StandardCard(std.TWO, std.SPADE)
        hand = std.StandardHand([ace, two])
        self.assertEqual(repr(hand), "<StandardHand:As,2s>")

    def test_hand_by_suit(self):
        spades = std.make_deck().by_suit(std.SPADE)
        self.assertEqual(str(spades), "AKQJT98765432s")

    def test_hand_by_rank(self):
        self.assertEqual(str(self.hands["aces"]), "As Ah Ad Ac")

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

    def test_sets(self):
        sets = {
            "deck": [self.hands["deck"].by_rank(r) for r in std.RANKS],
            "spades": [],
            "mixed": [std.StandardHand([std.StandardCard(r, std.SPADE),
                                        std.StandardCard(r, std.CLUB)])
                                       for r in std.RANKS[1:]],
            "aces": [self.hands["aces"]],
            "empty": [],
            "separate": [],
        }
        for hand in self.hands:
            self.assertEqual(std.find_sets(self.hands[hand]), sets[hand])

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
            "empty": [],
            "separate": [std.StandardHand([std.StandardCard(std.SEVEN,
                                          std.CLUB)]),
                         std.StandardHand([self.hands["spades"][0]])],
        }
        for hand in self.hands:
            self.assertEqual(std.find_flushes(self.hands[hand]),
                             flushes[hand])

    def test_straights(self):
        def count_straights(hand):
            return len(std.find_straights(hand))

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
        self.assertEqual(count_straights(self.hands["separate"]), 2)
