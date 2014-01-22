"""Functions for evaluating poker hands."""

import functools
import itertools

from pydeck import standard as std


@functools.total_ordering
class LongerStronger(object):

    """Comparator class, to use as a key when sorting hands.

    Prioritizes the longer hand. If two are the same length, prioritizes
    the one whose first card is higher-ranked. If those are the same,
    compares the ranks of the second cards, etc.

    """

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
        self_ranks = sorted([c.rank for c in self])
        other_ranks = sorted([c.rank for c in other])
        for i in range(len(self)):
            if self_ranks[i] != other_ranks[i]:
                return self_ranks[i] < other_ranks[i]
        return False


def all_best(hands):
    """Return all the hands in a list which are tied for best.

    See LongerStronger for a definition of best. If an empty list is
    passed, an empty list is returned.

    """
    if not hands:
        return []

    best = [hands[0]]
    for hand in hands[1:]:
        if LongerStronger(hand) == LongerStronger(best[0]):
            best.append(hand)
        elif LongerStronger(hand) > LongerStronger(best[0]):
            best = [hand]
    return best


def best_sets(hand, minimum=2):
    """Find the best sets in a hand, by LongerStronger. Returns a list."""
    return all_best(std.find_sets(hand, minimum))


def best_flushes(hand, minimum=1):
    """Find the best flushes in a hand, by LongerStronger. Returns a list."""
    return all_best(std.find_flushes(hand, minimum))


def best_straights(hand, minimum=1):
    """Find the best straights in a hand, by LongerStronger. Returns a list."""
    return all_best(std.find_straights(hand, minimum))


def find_full_houses(hand):
    """Find all the full houses in a hand.

    A full house is a set of three and a set of two. Returns a list of
    StandardHands. Each rank represented in a hand will only appear
    once among the full houses, even though you can make four sets of
    three or six pairs out of four of a kind. That is, if you pass in
    four kings and four sevens, you'll get two full houses out: kings
    over sevens, and sevens over kings. Which suits are used depends on
    the card order in the input hand.

    """
    full_houses = []
    triples = std.find_sets(hand, minimum=3)
    for triple in triples:
        triple = triple[0:3]
        remainder = hand - triple
        pairs = std.find_sets(remainder, minimum=2)
        for pair in pairs:
            pair = pair[0:2]
            full_houses.append(triple + pair)
    return full_houses

if __name__ == "__main__":
    deck = std.make_deck(shuffle=True)
    print deck.deal(13)
