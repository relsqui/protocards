#!/usr/bin/python

import random, itertools, functools


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

        rank = string[0].upper()
        suit = string[1].lower()
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
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        if self.rank == other.rank:
            return SUITS.find(self.suit) < SUITS.find(other.suit)
        else:
            return RANKS.find(self.rank) < RANKS.find(other.rank)


class Hand (object):
    def __init__ (self):
        self.cards = []

    def __repr__(self):
        return "<Hand:{}>".format(",".join([str(c) for c in self.cards]))

    def __str__(self):
        suit_strings = []
        for s in SUITS:
            cards = sorted(self.by_suit(s), reverse=True)
            if cards:
                suit_strings.append("".join([c.rank for c in cards]) + s)
        return " ".join(suit_strings)

    def sort(self):
        self.cards.sort(reverse=True)

    def by_suit(self, suit):
        suit = suit.lower()
        if suit not in SUITS:
            raise ValueError("Bad suit: {}".format(suit))
        return [c for c in self.cards if c.suit == suit]

    def by_rank(self, rank):
        rank = rank.upper()
        if rank not in RANKS:
            raise ValueError("Bad rank: {}".format(suit))
        return [c for c in self.cards if c.rank == rank]

    def shuffle(self):
        random.shuffle(self.cards)

    def append(self, card):
        if not isinstance (card, Card):
            raise TypeError("{} is not a card!".format(card))
        self.cards.append(card)

    def extend(self, cards):
        for c in cards:
            self.append(c)

    def pop(self):
        return self.cards.pop()

    def deal(self, count):
        dealt = []
        for i in range(count):
            dealt.append(self.pop())
        return dealt

def make_deck(shuffle = True):
    deck = Hand()
    deck.extend([Card(rank + suit) for suit, rank in itertools.product(SUITS, RANKS)])
    if shuffle:
        deck.shuffle()
    return deck

if __name__ == "__main__":
    deck = make_deck()
    hand = Hand()
    hand.extend(deck.deal(13))
    print hand
