#!/usr/bin/python


import random, itertools, functools

RANKS = "A23456789TJQK"
RANK_NAMES = {
    "A": "Ace",
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
    "K": "King"
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
        if rank not in "A23456789TJQK":
            raise ValueError("Bad rank: {}".format(rank))
        if suit not in "cdhs":
            raise ValueError("Bad suit: {}".format(suit))
        self.rank = rank
        self.suit = suit

        if rank == "A":
            self.value = 1
        elif rank in "TJQK":
            self.value = 10
        else:
            self.value = int(rank)

        self.name = "{} of {}".format(RANK_NAMES[rank], SUIT_NAMES[suit])

    def __str__(self):
        return self.rank + self.suit

    def __repr__(self):
        return 'Card("{}")'.format(str(self))

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        if self.suit == other.suit:
            return RANKS.find(self.rank) < RANKS.find(other.rank)
        else:
            return SUITS.find(self.suit) < SUITS.find(other.suit)


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

    def by_value(self, value):
        value = int(value)
        return [c for c in self.cards if c.value == value]

    def shuffle(self):
        random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()


if __name__ == "__main__":
    deck = Hand()
    for suit, rank in itertools.product(SUITS, RANKS):
        deck.add(Card(rank + suit))
    print deck
    deck.shuffle()
    print deck

    print

    hand = Hand()
    for i in range(5):
        hand.add(deck.pop())
    print hand
    hand.sort()
    print hand
