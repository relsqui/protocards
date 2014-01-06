"""Tools and definitions for a standard deck of 52 cards.

In addition to the classes and functions listed, provides constants for
the ranks TWO through ACE and suits CLUB through SPADE, along with a
list of each: RANKS and SUITS.

"""

import functools
import itertools

from pydeck import base


@functools.total_ordering
class Rank(base.CardProperty):

    """A card's rank.

    Ranks can be sorted; the key is their index in RANKS, which can be
    retrieved from the `.order` property.

    """

    def __le__(self, other):
        return self.order < other.order

    @property
    def order(self):
        return RANKS.index(self)


@functools.total_ordering
class Suit(base.CardProperty):

    """A card's suit.

    Differs from base.CardProperty by having a lowercase default
    `.short`. Suits can be sorted; the key is their index in SUITS,
    which can be retrieved from the `.order` property.

    """

    def __init__(self, *args, **kwargs):
        super(Suit, self).__init__(*args, **kwargs)
        self.short = self.short.lower()

    def __le__(self, other):
        return self.order < other.order

    @property
    def order(self):
        return SUITS.index(self)


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

    Initialize with one member each of RANKS and SUITS. Cards can
    be sorted; they'll be ordered by rank first, then suit, according
    to the order in RANKS and SUITS.

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
            return self.suit < other.suit
        return self.rank < other.rank


class StandardHand(base.Hand):

    """A hand of standard playing cards.

    StandardHands can be compared naively. One StandardHand is greater
    than another if it is longer; or, if they are the same length, its
    highest-ranked card has greater rank; or, if their highest cards
    have the same rank, if its second-highest-ranked card has greater
    rank, and so on. Note that, unlike for StandardCards, suit is not
    taken into account.

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

    def __eq__(self, other):
        return sorted([c.rank for c in self]) == sorted([c.rank for c in other])

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if len(self) != len(other):
            return len(self) < len(other)
        for i in range(len(self)):
            if self[i].rank != other[i].rank:
                return self[i].rank < other[i].rank
        return False

    def __gt__(self, other):
        return not (self < other or self == other)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def by_suit(self, suit):
        """Return all cards of `suit`, without removing them."""
        return self.__class__([c for c in self if c.suit == suit])

    def by_rank(self, rank):
        """Return all cards of `rank`, without removing them."""
        return self.__class__([c for c in self if c.rank == rank])


def make_deck(shuffle=False):
    """Return a StandardHand of all 52 cards; optionally, shuffle it."""
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
