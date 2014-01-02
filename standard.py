#!/usr/bin/python

import functools, itertools

import base


TWO = base.CardProperty("2", "Two")
THREE = base.CardProperty("3", "Three")
FOUR = base.CardProperty("4", "Four")
FIVE = base.CardProperty("5", "Five")
SIX = base.CardProperty("6", "Six", "Sixes")
SEVEN = base.CardProperty("7", "Seven")
EIGHT = base.CardProperty("8", "Eight")
NINE = base.CardProperty("9", "Nine")
TEN = base.CardProperty("T", "Ten")
JACK = base.CardProperty("J", "Jack")
QUEEN = base.CardProperty("Q", "Queen")
KING = base.CardProperty("K", "King")
ACE = base.CardProperty("A", "Ace")

CLUB = base.CardProperty("c", "Club")
DIAMOND = base.CardProperty("d", "Diamond")
HEART = base.CardProperty("h", "Heart")
SPADE = base.CardProperty("s", "Spade")

RANKS = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]
SUITS = [CLUB, DIAMOND, HEART, SPADE]


@functools.total_ordering
class StandardCard (base.EqualityMixin):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.short = self.rank.short + self.suit.short
        self.name = "{} of {}".format(rank.name.title(), suit.plural.title())

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<StandardCard:{}>'.format(self.short)

    def __lt__(self, other):
        if self.rank == other.rank:
            return SUITS.index(self.suit) < SUITS.index(other.suit)
        else:
            return RANKS.index(self.rank) < RANKS.index(other.rank)


class StandardHand (base.Hand):
    def __str__(self):
        suit_strings = []
        for s in SUITS:
            cards = sorted(self.by_suit(s), reverse=True)
            if cards:
                suit_strings.append("".join([c.rank.short for c in cards]) + s.short)
        return " ".join(suit_strings)

    def __repr__(self):
        return "<StandardHand:{}>".format(",".join([c.short for c in self]))

    def by_suit(self, suit):
        return StandardHand([c for c in self if c.suit == suit])

    def by_rank(self, rank):
        return StandardHand([c for c in self if c.rank == rank])


def make_deck(shuffle = False):
    deck = StandardHand([StandardCard(rank, suit) for suit, rank in itertools.product(SUITS, RANKS)])
    if shuffle:
        deck.shuffle()
    return deck


if __name__ == "__main__":
    deck = make_deck(shuffle = True)
    print deck.deal(13)
