## pydeck

Generalized card classes and game-specific libraries.


### base.py
Provides tools for building card, deck, and game types with.

##### classes
* `CardProperty(name, plural=None, short=None)`
  * initialize with a string name and, optionally, short and plural versions
    of that name.
    * if no plural is provided, `name + "s"` will be used.
    * if no short name is provided, `name[0]` will be used.
  * no exposed methods.
  * properties are just `short`, `name`, and `plural`.

* `Hand([Card, ...])`
  * initialize, optionally, with a sequence of `Card`s (e.g. another `Hand`).
  * subclasses `UserList.UserList`, and therefore behaves like a `list` in
    terms of standard methods, adding and multiplying, and slicing.
    * slices return another `Hand`.
  * additional methods:
    * `.shuffle()` is the opposite of `.sort()` (and also works in-place)
    * `.deal(count)` pops off `count` items and returns them as a `Hand`.
  * no exposed properties.


### standard.py
Implements standard playing cards, with four suits, thirteen ranks, etc.

##### constants
* `TWO` through `NINE`, `JACK`, `QUEEN`, `KING`, and `ACE` are `Rank`s.
* `CLUB`, `DIAMOND`, `HEART`, and `SPADE` are `Suit`s.
* `RANKS` is a list of `TWO` through `ACE`, in that order.
* `SUITS` is a list of `CLUB`, `DIAMOND`, `HEART`, and `SPADE`, in that order.

##### classes
* `Rank` and `Suit` subclass `base.CardProperty`, mostly for naming clarity.
  * `Suit` lowercases its `.short`.

* `StandardCard(Rank, Suit)`
  * no exposed methods.
  * properties:
    * `.rank` (its `Rank`) and `.suit` (its `Suit`).
    * `.short` = `.rank.short + .suit.short`, e.g. "Jh" for the Jack of
      Hearts.
    * `.name` is automatically generated as "Rank of Suit", so capitalized.
  * can be compared and sorted; will use `.rank` first, then `.suit`, as
    ordered in `RANKS` and `SUITS`.

* `StandardHand([Card, ...])`
  * subclasses `base.Hand`.
  * additional methods:
    * `.by_rank(Rank)` and `.by_suit(Suit)` return a new `StandardHand`
      composed of the cards in this one which have the rank or suit given.
  * adds a pretty string representation in which cards are grouped by suit and
    sorted by rank (without altering the actual order).

##### functions
* `make_deck(shuffle=False)`
   * returns a `StandardHand` populated with one of every unique pair of rank
     and suit.
   * call with `shuffle=True` to shuffle the deck before returning it.


### cribbage.py

##### constants
* `RANKS` is `standard.RANKS` but with `standard.ACE` at the beginning.
* `SUITS` is the same as `standard.SUITS`.

##### functions
* `score_hand(standard.StandardHand, turned=None, crib=False, dealer=False)`
  * returns a dictionary whose keys are ("fifteens", "pairs", "runs", "flush",
    "heels", and "nobs"), and whose values are the points earned by that hand
    for each type of score.
    * `sum(score_hand(...).values())` gives total score.
  * the turned card, if provided, adds some additional scoring potential:
    * it's included in the hand for counting fifteens, pairs, and runs.
    * nobs may be scored, based on its suit.
    * with `dealer=True`, heels may be scored, based on its suit.
    * with `crib=True`, it must be included in a flush for the flush to count.

* `score_fifteens(standard.StandardHand)`,
  `score_pairs(standard.StandardHand)`,
  `score_runs(standard.StandardHand)`
  * each returns a partial score, looking at only one aspect of the hand.

* `check_flush(standard.StandardHand)`
  * returns `True` if all cards in the hand have the same `.suit`, `False`
    otherwise.

* `value(standard.StandardCard)`
  * returns the point value of the card: 1 for an ace, 10 for an honor, and
    face value for anything else.


### example

```
>>> import standard
>>> deck = standard.make_deck(shuffle=True)
>>> hand = deck.deal(4)
>>> print hand
9d 84h Js
>>> turned = deck.pop()
>>> print turned
Nine of Spades
>>> 
>>> import cribbage
>>> cribbage.score_hand(hand, turned=turned)
{'nobs': 1, 'pairs': 2}
```

___
I originally wrote this because I wanted to know what the cribbage score for a
whole deck of cards was. Here's the answer, if you're curious:

```
relsqui@barrett:~/cribbage-scorer$ cat score_the_deck.py 
#!/usr/bin/python

import cards, cribbage

score = cribbage.score_hand(standard.make_deck())
for k, v in score.items():
    print k, "for", v
print "total:", sum(score.values())


relsqui@barrett:~/cribbage-scorer$ ./score_the_deck.py 
fifteens for 34528
runs for 872415232
pairs for 156
total: 872449916
```

Plus 1-2 for heels/nobs, depending on the turned card and whether you're
dealing.
