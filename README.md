## pydeck

Generalized card classes and game-specific libraries.


### base.py
Provides tools for building card, deck, and game types with.

##### classes
* `CardProperty(name, plural = None, short = None)`
  * initialize with a string name and, optionally, short and plural versions
    of that name.
    * if no plural is provided, `name + "s"` will be used.
    * if no short name is provided, `name[0]` will be used.
  * no exposed methods.
  * attributes are just `short`, `name`, and `plural`.

* `Hand([Card, ...])`
  * initialize, optionally, with a sequence of `Card`s (e.g. another `Hand`).
  * subclasses `UserList.UserList`, and therefore behaves like a `list` in
    terms of standard methods, adding and multiplying, and slicing.
    * slices return another `Hand`.
  * additional methods:
    * `.shuffle()` is the opposite of `.sort()` (and also works in-place)
    * `.deal(count)` pops off `count` items and returns them as a `Hand`.
  * no exposed attributes.


### standard.py
Implements standard playing cards, with four suits, thirteen ranks, etc.

##### constants
* `TWO` through `NINE`, `JACK`, `QUEEN`, `KING`, and `ACE` are `Rank`s.
* `CLUB`, `DIAMOND`, `HEART`, and `SPADE` are `Suit`s.
* `RANKS` is a list of `TWO` through `ACE`, in that order.
* `SUITS` is a list of `CLUB`, `DIAMOND`, `HEART`, and `SPADE`, in that order.

##### classes
* `Rank` and `Suit` subclass `CardProperty`, mostly for naming clarity.
  * `Suit` lowercases its `.short`.

* `StandardCard(rank, suit)`
  * initialize with a `CardProperty` from `RANKS` and another one from `SUITS`,
    e.g. `Card(JACK, HEART)` to make a Jack of Hearts.
  * no exposed methods.
  * attributes:
    * `.rank` and `.suit`, each a `CardProperty`
    * `.short` = `.rank.short` + `.suit.short`, e.g. "Jh" for the Jack of
      Hearts.
    * `.name` is "Rank of Suit", using rank.name.title() and
      suit.plural.title().
  * can be compared and sorted; will use rank first, then suit, as ordered
    in `RANKS` and `SUITS`.

* `StandardHand([Card, ...])`
  * subclasses `Hand`; has its methods, and also:
    * `.by_rank(rank)` and `.by_suit(suit)` return a new `StandardHand`
      composed of the cards in this one which have the rank or suit given.
  * adds a pretty string representation in which cards are grouped by suit and
    sorted by rank (without altering the actual order).

##### functions
* `make_deck(shuffle = False)`
   * returns a `StandardHand` populated with one of every unique pair of rank
     and suit.
   * call with `shuffle = True` to shuffle the deck before returning it.


### cribbage.py

##### constants
* overrides `standard.RANKS` to put `standard.ACE` at the beginning.

##### functions
* `score_hand(StandardHand, turned = None, crib = False, dealer = False)`
  * returns a dictionary whose keys are strings giving score type ("fifteens",
    "pairs", "runs", "flush", "heels", or "nobs"), and whose values are score
    numbers.
    * `sum(score_hand(StandardHand).values())` gives total score.
  * the turned card, if provided, will be included in the hand for counting
    fifteens, pairs, and runs, and possibly flushes, heels, or nobs depending
    on the other options. the boolean options only matter when a turned card
    was passed:
    * if `crib = True`, the hand will be scored like a crib, i.e. flushes will
      only count if they include the turned card.
    * if `dealer = True`, heels may be scored; otherwise, nobs may be scored.

* `score_fifteens(StandardHand)`, `score_pairs(StandardHand)`,
  `score_runs(StandardHand)`
  * each returns a partial score, looking at only one aspect of the hand.

* `check_flush(StandardHand)`
  * returns `True` if all cards in the hand have the same `.suit`, `False`
    otherwise.

* `value(StandardCard)`
  * returns the point value of the card: 1 for an ace, 10 for an honor, and
    face value for anything else.


### example

```
>>> import standard
>>> deck = standard.make_deck(shuffle = True)
>>> hand = deck.deal(4)
>>> print hand
9d 84h Js
>>> turned = deck.pop()
>>> print turned
Nine of Spades
>>> 
>>> import cribbage
>>> cribbage.score_hand(hand, turned = turned)
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
