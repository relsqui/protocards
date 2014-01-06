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
        """Return the Rank's index in RANKS."""
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
        """Return the Suit's index in SUITS."""
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


class StandardHand(base.Hand):

    """A hand of standard playing cards."""

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


@functools.total_ordering
class LongerStronger(object):

    """Comparator class, to use as a key when sorting hands."""

    def __init__(self, obj, *args):
        self.obj = obj

    def __eq__(self, other):
        self = self.obj
        other = other.obj
        return (sorted([c.rank for c in self]) ==
                sorted([c.rank for c in other]))

    def __lt__(self, other):
        self = self.obj
        other = other.obj
        if len(self) != len(other):
            return len(self) < len(other)
        for i in range(len(self)):
            if self[i].rank != other[i].rank:
                return self[i].rank < other[i].rank
        return False


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


def best_flush(hand):
    """Find the best flush in a hand.

    Returns a StandardHand of the highest flush in the hand provided.
    If one of the flushes is longest, that one is returned; else, the
    one with the highest-ranked highest card is returned, or the
    highest-ranked second-highest card if the first are equal, and so
    on. If the longest flushes share all their card ranks, the one with
    the highest suit is returned.

    If the given hand is empty, the returned hand is also empty.

    """
    if not len(hand):
        return StandardHand()

    def card_ranks(hand):
        return sorted([c.rank for c in hand])

    all_flushes = [hand.by_suit(s) for s in SUITS]
    best_by_rank = max(all_flushes, key=LongerStronger)
    all_best = [f for f in all_flushes if card_ranks(f) ==
                                          card_ranks(best_by_rank)]
    best = max(all_best, key=lambda f: f[0].suit)
    return best


if __name__ == "__main__":
    deck = make_deck(shuffle=True)
    print deck.deal(13)
