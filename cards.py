#!/usr/bin/python


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
            card_string = self.rank + self.suit
            return card_string


class Hand (object):
    def __init__ (self):
        self.cards = []

    def add(self, card):
        if not isinstance (card, Card):
            raise TypeError("{} is not a card!".format(card))
        self.cards.append(card)
        return self

    def by_suit(self, suit):
        suit = suit.lower()
        if suit not in SUIT_NAMES:
            raise ValueError("Bad suit: {}".format(suit))
        suited = [c for c in self.cards if c.suit == suit]
        return suited

    def __str__(self):
        hand_string = ""
        for suit in SUIT_NAMES:
            ranks = [c.rank for c in self.by_suit(suit)]
            if ranks:
                hand_string += "".join(ranks) + suit + " "
        return hand_string


if __name__ == "__main__":
    import sys

    hand = Hand()
    for string in sys.argv[1:]:
        try:
            hand.add(Card(string))
        except ValueError as e:
            print "Error parsing '{}': {}".format(string, e)

    print hand
