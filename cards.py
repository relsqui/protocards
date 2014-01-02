#!/usr/bin/python

import random, itertools, functools, UserList


RANKS = "23456789TJQKA"
RANK_NAMES = {
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
    "T": "Ten",
    "J": "Jack",
    "Q": "Queen",
    "K": "King",
    "A": "Ace"
}

SUITS = "cdhs"
SUIT_NAMES = {
    "c": "Clubs",
    "d": "Diamonds",
    "h": "Hearts",
    "s": "Spades"
}


@functools.total_ordering
class Card (object):
    def __init__(self, string):
        string = string.strip()
        if len(string) != 2:
            raise ValueError("Card string should be exactly two characters.")

        rank = string[0]
        suit = string[1]
        if rank not in RANKS:
            raise ValueError("Bad rank: {}".format(rank))
        if suit not in SUITS:
            raise ValueError("Bad suit: {}".format(suit))
        self.rank = rank
        self.suit = suit

        self.name = "{} of {}".format(RANK_NAMES[rank], SUIT_NAMES[suit])

    def __str__(self):
        return self.rank + self.suit

    def __repr__(self):
        return 'Card("{}")'.format(str(self))

    def __eq__(self, other):
        try:
            return self.rank == other.rank and self.suit == other.suit
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.rank == other.rank:
            return SUITS.find(self.suit) < SUITS.find(other.suit)
        else:
            return RANKS.find(self.rank) < RANKS.find(other.rank)


class Hand (UserList.UserList):
    def __str__(self):
        suit_strings = []
        for s in SUITS:
            cards = sorted(self.by_suit(s), reverse=True)
            if cards:
                suit_strings.append("".join([c.rank for c in cards]) + s)
        return " ".join(suit_strings)

    def __repr__(self):
        return "Hand({})".format(", ".join(map(repr, self)))

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
    deck = Hand([Card(rank + suit) for suit, rank in itertools.product(SUITS, RANKS)])
    if shuffle:
        deck.shuffle()
    return deck


if __name__ == "__main__":
    deck = make_deck(shuffle = True)
    print deck.deal(13)
