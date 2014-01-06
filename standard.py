"""Tools and definitions for a standard deck of 52 cards.

In addition to the classes and functions listed, provides constants for
the ranks TWO through ACE and suits CLUB through SPADE, along with a
list of each: RANKS and SUITS.

"""

import functools
import itertools

from pydeck import base


class Rank(base.CardProperty):

    """Subclass of `pydeck.base.CardProperty` for symmetry with `Suit`."""

    pass


class Suit(base.CardProperty):

    """Subclass of `pydeck.base.CardProperty`. Lowercases its `.short`."""

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

RANKS = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT,
         NINE, TEN, JACK, QUEEN, KING, ACE]
SUITS = [CLUB, DIAMOND, HEART, SPADE]


@functools.total_ordering
class StandardCard(base.Card):

    """A regular playing card with a rank and a suit.

    Initialize with members of `RANKS` and `SUITS`. Raises ValueError
    if anything else is provided.

    Attributes:
        rank, suit - As provided.
        name       - "Rank of Suits" in title case.
        short      - rank.short + suit.short

    """

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


class StandardHand(base.Hand):

    """A hand of standard playing cards.

    Raises TypeError if a non-`StandardCard` is passed in.

    """

    def __str__(self):
        suit_strings = []
        for suit in reversed(SUITS):
            cards = sorted(self.by_suit(suit), reverse=True)
            if cards:
                ranks = "".join([c.rank.short for c in cards])
                suit_strings.append(ranks + suit.short)
        return " ".join(suit_strings)

    def __repr__(self):
        return "<{}:{}>".format(self.__class__.__name__,
                                ",".join([c.short for c in self]))

    def by_suit(self, suit):
        """Return all cards of `suit`, without removing them."""
        return self.__class__([c for c in self if c.suit == suit])

    def by_rank(self, rank):
        """Return all cards of `rank`, without removing them."""
        return self.__class__([c for c in self if c.rank == rank])


def make_deck(shuffle=False):
    """Return a `StandardHand` of all 52 cards; optionally, shuffle it."""
    deck = StandardHand([StandardCard(rank, suit)
                         for suit, rank in itertools.product(SUITS, RANKS)])
    if shuffle:
        deck.shuffle()
    return deck


def find_pairs(hand):
    """Find all pairs (two cards with the same rank) in a hand.

    Returns a list of tuples of cards.

    """
    pairs = []
    for rank in RANKS:
        pairs.extend(itertools.combinations(hand.by_rank(rank), 2))
    return pairs


def find_flushes(hand):
    """Find the longest flush(es) in a hand.

    Returns a list of tuples of cards with the same suit. If there is a
    single longest flush in the hand, the list will contain only one
    tuple. If two or more flushes are tied for longest, they will all
    be returned (and any others will be ignored). If an empty hand is
    passed, an empty list will be returned.

    """
    if not len(hand):
        return []
    flushes = [[]]
    for suit in SUITS:
        by_suit = tuple(hand.by_suit(suit))
        if len(by_suit) > len(flushes[0]):
            flushes = [by_suit]
        elif len(by_suit) == len(flushes[0]):
            flushes.append(by_suit)
    return flushes


if __name__ == "__main__":
    deck = make_deck(shuffle=True)
    print deck.deal(13)
