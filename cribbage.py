#!/usr/bin/python

import itertools
from operator import mul

import cards
cards.RANKS = "A23456789TJQK"


def value(card):
    if card.rank == "A":
        value = 1
    elif card.rank.isdigit():
        value = int(card.rank)
    else:
        value = 10
    return value

def score_pairs(hand):
    pairs = 0
    for r in cards.RANKS:
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

    values = [value(c) for c in hand.cards]
    fifteens = count_subsums(15, values)
    return fifteens * 2

def score_runs(hand):
    rank_counts = []
    for r in cards.RANKS:
        rank_counts.append(len(hand.by_rank(r)))

    run_slices = []
    begin = 0
    for end in range(len(cards.RANKS)):
        if rank_counts[end] == 0:
            if end > begin:
                run_slices.append(rank_counts[begin:end])
            begin = end + 1
    if begin < len(cards.RANKS):
        run_slices.append(rank_counts[begin:])

    run_score = 0
    for run in run_slices:
        if len(run) > 2:
            run_score += reduce(mul, run, len(run))
    return run_score

def check_flush(hand):
    if len(hand.cards) == len(hand.by_suit(hand.cards[0].suit)):
        return True
    return False

def score_hand(hand, turned = None, crib = False, dealer = False):
    score = {}
    test_hand = cards.Hand()
    test_hand.extend(hand.cards)
    if turned:
        test_hand.append(turned)

    fifteens = score_fifteens(test_hand)
    if fifteens:
        score["fifteens"] = fifteens

    pairs = score_pairs(test_hand)
    if pairs:
        score["pairs"] = pairs

    runs = score_runs(test_hand)
    if runs:
        score["runs"] = runs

    if check_flush(hand):
        if turned and hand.cards[0].suit == turned.suit:
            score["flush"] = len(hand.cards) + 1
        elif not turned or not crib:
            score["flush"] = len(hand.cards)

    if turned and dealer:
        if turned.rank == "J":
            score["heels"] = 2
    elif turned and cards.Card("J" + turned.suit) in hand.cards:
        score["nobs"] = 1

    return score


if __name__ == "__main__":
    from random import getrandbits

    def rand_bool():
        return not getrandbits(1)

    deck = cards.make_deck()
    hand = cards.Hand()
    hand.extend(deck.deal(4))
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
    for k, v in score.items():
        print k, "for", v
    print "total:", sum(score.values())
