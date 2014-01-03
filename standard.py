#!/usr/bin/python

import functools, itertools

import base


class Rank (base.CardProperty):
    pass

class Suit (base.CardProperty):
    def __init__(self, *args, **kwargs):
        super(Suit, self).__init__(*args, **kwargs)
        self.short = self.short.lower()

TWO = Rank("Two", short="2")
THREE = Rank("Three", short="3")
FOUR = Rank("Four", short="4")
FIVE = Rank("Five", short="5")
SIX = Rank("Six", plural="Sixes", short="6")
SEVEN = Rank("Seven", short="7")
EIGHT = Rank("Eight", short="8")
NINE = Rank("Nine", short="9")
TEN = Rank("Ten")
JACK = Rank("Jack")
QUEEN = Rank("Queen")
KING = Rank("King")
ACE = Rank("Ace")

CLUB = Suit("Club")
DIAMOND = Suit("Diamond")
HEART = Suit("Heart")
SPADE = Suit("Spade")

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
        return '<{}:{}>'.format(self.__class__.__name__, self.short)

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
        return "<{}:{}>".format(self.__class__.__name__, ",".join([c.short for c in self]))

    def by_suit(self, suit):
        return self.__class__([c for c in self if c.suit == suit])

    def by_rank(self, rank):
        return self.__class__([c for c in self if c.rank == rank])


def make_deck(shuffle = False):
    deck = StandardHand([StandardCard(rank, suit) for suit, rank in itertools.product(SUITS, RANKS)])
    if shuffle:
        deck.shuffle()
    return deck


if __name__ == "__main__":
    deck = make_deck(shuffle = True)
    print deck.deal(13)
