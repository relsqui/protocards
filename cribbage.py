#!/usr/bin/python

import itertools
from random import getrandbits

import cards
cards.RANKS = "A23456789TJQK"


def rand_bool():
    return not getrandbits(1)

def value(card):
    if card.rank == "A":
        return 1
    elif card.rank.isdigit():
        return int(card.rank)
    else:
        return 10

def count_pairs(hand):
    pairs = 0
    for r in cards.RANKS:
        same = float(len(hand.by_rank(r)))
        pairs += (same * ((same - 1) / 2))
    return int(pairs)

def count_fifteens(hand):
    fifteens = 0
    for i in range(2, 10):
        books = itertools.combinations(hand.cards, i)
        for b in books:
            if sum([value(c) for c in b]) == 15:
                fifteens += 1
    return fifteens

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

    fifteens = count_fifteens(test_hand)
    if fifteens:
        score["fifteens"] = fifteens * 2

    pairs = count_pairs(test_hand)
    if pairs:
        score["pairs"] = pairs * 2

    if check_flush(hand):
        if turned and hand.cards[0].suit == turned.suit:
            score["flush"] = len(hand.cards) + 1
        elif not turned or not crib:
            score["flush"] = len(hand.cards)

    if turned and dealer:
        if turned.rank == "J":
            score["heels"] = 2
    elif turned and cards.Card("J" + turned.suit) in hand.cards:
        score["nibs"] = 1

    return score


if __name__ == "__main__":
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
