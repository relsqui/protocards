"""Functions for evaluating poker hands."""

import functools
import itertools

from pydeck import standard as std


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


def find_sets(hand):
    """Find all sets (two or more cards with the same rank) in a hand.

    Returns a list of StandardHands.

    """
    if not len(hand):
        return std.StandardHand()
    sets = []
    for rank in std.RANKS:
        by_rank = hand.by_rank(rank)
        if len(by_rank) > 1:
            sets.append(by_rank)
    return sets


def best_set(hand):
    """Find the best set of like rank in a hand. Returns a StandardHand."""
    sets = find_sets(hand)
    if not len(sets):
        return std.StandardHand()
    best_length = len(max(sets, key=len))
    longest = [s for s in sets if len(s) == best_length]
    return max(longest, key=lambda s: s[0].rank)


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
    def card_ranks(hand):
        return sorted([c.rank for c in hand])

    if not len(hand):
        return std.StandardHand()
    all_flushes = [hand.by_suit(s) for s in std.SUITS]
    best_by_rank = max(all_flushes, key=LongerStronger)
    all_best = [f for f in all_flushes if card_ranks(f) ==
                                          card_ranks(best_by_rank)]
    return max(all_best, key=lambda f: f[0].suit)


if __name__ == "__main__":
    deck = std.make_deck(shuffle=True)
    print deck.deal(13)
