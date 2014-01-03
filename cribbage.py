#!/usr/bin/python

from operator import mul

import standard


RANKS = [standard.RANKS[-1]] + standard.RANKS[:-1]
SUITS = standard.SUITS


def value(card):
    return min(RANKS.index(card.rank) + 1, 10)


def score_pairs(hand):
    pairs = 0
    for r in RANKS:
        same = float(len(hand.by_rank(r)))
        pairs += (same * ((same - 1) / 2))
    return int(pairs) * 2


def score_fifteens(hand):
    def count_subsums(target, numbers):
        subsums = 0
        if sum(numbers) == target:
            subsums = 1
        elif sum(numbers) > target:
            for i, n in enumerate(numbers):
                if n == target:
                    subsums += 1
                elif n < target:
                    subsums += count_subsums(target - n, numbers[i+1:])
        return subsums

    values = [value(c) for c in hand]
    fifteens = count_subsums(15, values)
    return fifteens * 2


def score_runs(hand):
    rank_counts = []
    for r in RANKS:
        rank_counts.append(len(hand.by_rank(r)))

    run_slices = []
    begin = 0
    for end in range(len(RANKS)):
        if rank_counts[end] == 0:
            if end > begin:
                run_slices.append(rank_counts[begin:end])
            begin = end + 1
    if begin < len(RANKS):
        run_slices.append(rank_counts[begin:])

    run_score = 0
    for run in run_slices:
        if len(run) > 2:
            run_score += reduce(mul, run, len(run))
    return run_score


def check_flush(hand):
    if len(hand) == len(hand.by_suit(hand[0].suit)):
        return True
    return False


def score_hand(hand, turned=None, crib=False, dealer=False):
    score = {"fifteens": 0, "pairs": 0, "runs": 0, "flush": 0,
             "heels": 0, "nobs": 0}
    test_hand = standard.StandardHand(hand)
    if turned:
        test_hand.append(turned)

    score["fifteens"] = score_fifteens(test_hand)
    score["pairs"] = score_pairs(test_hand)
    score["runs"] = score_runs(test_hand)

    if check_flush(hand):
        if turned and hand[0].suit == turned.suit:
            score["flush"] = len(hand) + 1
        elif not turned or not crib:
            score["flush"] = len(hand)

    if turned and dealer and turned.rank == standard.JACK:
        score["heels"] = 2
    elif turned and standard.StandardCard(standard.JACK, turned.suit) in hand:
        score["nobs"] = 1

    return score


if __name__ == "__main__":
    from random import getrandbits

    def rand_bool():
        return not getrandbits(1)

    deck = standard.make_deck(shuffle = True)
    hand = deck.deal(4)
    turned = deck.pop()

    dealing = rand_bool()
    cribbing = rand_bool()

    score = score_hand(hand, turned=turned, dealer=dealing, crib=cribbing)

    if dealing:
        print "dealing."
    if cribbing:
        print "counting crib."
    print "turned:", turned
    print hand
    print
    for reason, points in score.items():
        if points:
            print reason, "for", points
    print "total:", sum(score.values())
