#!/usr/bin/python

import random, itertools, functools, UserList


class CardProperty(object):
    def __init__(self, short, name, plural = None):
        self.short = short
        self.name = name
        if plural is None:
            self.plural = self.name + "s"
        else:
            self.plural = plural

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<CardProperty:{}>".format(self.name)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


TWO = CardProperty("2", "Two")
THREE = CardProperty("3", "Three")
FOUR = CardProperty("4", "Four")
FIVE = CardProperty("5", "Five")
SIX = CardProperty("6", "Six", "Sixes")
SEVEN = CardProperty("7", "Seven")
EIGHT = CardProperty("8", "Eight")
NINE = CardProperty("9", "Nine")
TEN = CardProperty("T", "Ten")
JACK = CardProperty("J", "Jack")
QUEEN = CardProperty("Q", "Queen")
KING = CardProperty("K", "King")
ACE = CardProperty("A", "Ace")

CLUB = CardProperty("c", "Club")
DIAMOND = CardProperty("d", "Diamond")
HEART = CardProperty("h", "Heart")
SPADE = CardProperty("s", "Spade")

RANKS = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]
SUITS = [CLUB, DIAMOND, HEART, SPADE]


@functools.total_ordering
class Card (object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.short = self.rank.short + self.suit.short
        self.name = "{} of {}".format(rank.name.title(), suit.plural.title())

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Card:{}>'.format(self.short)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.rank == other.rank:
            return SUITS.index(self.suit) < SUITS.index(other.suit)
        else:
            return RANKS.index(self.rank) < RANKS.index(other.rank)


class Hand (UserList.UserList):
    def __str__(self):
        suit_strings = []
        for s in SUITS:
            cards = sorted(self.by_suit(s), reverse=True)
            if cards:
                suit_strings.append("".join([c.rank.short for c in cards]) + s.short)
        return " ".join(suit_strings)

    def __repr__(self):
        return "<Hand:{}>".format(",".join([c.short for c in self]))

    def by_suit(self, suit):
        return [c for c in self if c.suit == suit]

    def by_rank(self, rank):
        return [c for c in self if c.rank == rank]

    def shuffle(self):
        random.shuffle(self)

    def deal(self, count):
        if count > len(self):
            raise IndexError("Not enough cards in Hand")
        dealt = self[:count]
        del self[:count]
        return dealt


def make_deck(shuffle = False):
    deck = Hand([Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS)])
    if shuffle:
        deck.shuffle()
    return deck


if __name__ == "__main__":
    deck = make_deck(shuffle = True)
    print deck.deal(13)
