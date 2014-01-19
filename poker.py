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
        for i in range(len(self)):
            if self[i].rank != other[i].rank:
                return self[i].rank < other[i].rank
        return False


def best_sets(hand):
    """Find the best sets in a hand.

    Returns a list of StandardHands of the highest sets in the hand
    provided. See LongerStronger for a definition of "highest." If
    there is a single best set, the list will only have one element;
    otherwise, all elements will be tied for length and rank.

    If an empty hand is passed, an empty list is returned.

    """
    sets = std.find_sets(hand)
    if not len(sets):
        return []
    best_length = len(max(sets, key=len))
    longest = [s for s in sets if len(s) == best_length]
    best_rank = max(longest, key=lambda s: s[0].rank)[0].rank
    return [s for s in longest if s[0].rank == best_rank]


def best_flushes(hand):
    """Find the best flushes in a hand.

    Returns a list of StandardHands of the highest flushes in the hand
    provided. See LongerStronger for a definition of "highest." If
    there is a single best flush, the list will only have one element;
    otherwise, all elements will be tied for rank and length.

    If an empty hand is passed, an empty list is returned.

    """
    def card_ranks(hand):
        return sorted([c.rank for c in hand])

    if not len(hand):
        return []
    all_flushes = std.find_flushes(hand)
    best = max(all_flushes, key=LongerStronger)
    return [f for f in all_flushes if card_ranks(f) == card_ranks(best)]


if __name__ == "__main__":
    deck = std.make_deck(shuffle=True)
    print deck.deal(13)
