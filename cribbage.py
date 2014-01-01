#!/usr/bin/python

import sys

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

SUIT_NAMES = {
    "c": "Clubs",
    "d": "Diamonds",
    "h": "Hearts",
    "s": "Spades"
}

class Card (object):
    def __init__ (self, string):
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


for string in sys.argv[1:]:
    try:
        card = Card(string)
        print "{} ({})".format(card.name, card.value)
    except ValueError as e:
        print "Error parsing '{}': {}".format(string, e)
