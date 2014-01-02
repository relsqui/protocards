## cribbage-scorer

Some basic card classes and a cribbage scoring library.


### cards.py

##### constants
* `RANKS` = "23456789TJQKA"
* `SUITS` = "cdhs"
* dictionaries `RANK_NAMES` and `SUIT_NAMES` map the above to titlecased words.
* override these to reorder rank and suit values, or to change the deck type or
  display characters.
  * any new ranks or suits should be added to `RANK_NAMES` and `SUIT_NAMES`.
  * non-unique characters in `RANKS` and `SUITS` aren't supported and may
    cause unusual behavior.

##### classes
* `Card(string)`
  * initialize with a two-character string of which the first comes from
    `RANKS` and the second comes from `SUITS`, e.g "Jh" for the Jack of Hearts.
    * invalid rank + suit strings raise `ValueError`.
  * no exposed methods.
  * attributes:
    * `.rank` and `.suit` (single characters, as initialized).
    * `.name` = "Rank of Suit" as defined by `RANK_NAMES` and `SUIT_NAMES`
  * can be compared and sorted; will use rank first, then suit, as ordered
    in `RANKS` and `SUITS`.

* `Hand([Card, ...])`
  * initialize, optionally, with a sequence of `Card`s (e.g. another `Hand`).
  * subclasses `UserList.UserList`, and therefore behaves like a `list` in
    terms of standard methods, adding and multiplying, and slicing.
    * slices return another `Hand`.
  * additional methods:
    * `.shuffle()` is the opposite of `.sort()` (and also works in-place)
    * `.deal(count)` pops off `count` items and returns them as a `Hand`.
    * `.by_rank(rank)` and `.by_suit(suit)` return a new `Hand` containing all
      cards in the first `Hand` of the given rank or suit.
  * no exposed attributes.

##### functions
* `make_deck(shuffle = False)`
   * returns a `Hand` populated with one of every unique card possible given
     the values of `RANKS` and `SUITS`.
   * call with `shuffle = True` to shuffle the deck before returning it.


### cribbage.py

##### constants
* overrides `cards.RANKS` to "A23456789TJQK", making aces sort low.

##### functions
* `score_hand(Hand, turned = None, crib = False, dealer = False)`
  * returns a dictionary whose keys are strings giving score type ("fifteens",
    "pairs", "runs", "flush", "heels", or "nobs"), and whose values are score
    numbers.
    * `sum(score_hand(Hand).values())` gives total score.
  * the turned card, if provided, will be included in the hand for counting
    fifteens, pairs, and runs, and possibly flushes, heels, or nobs depending
    on the other options. the boolean options only matter when a turned card
    was passed:
    * if `crib = True`, the hand will be scored like a crib, i.e. flushes will
      only count if they include the turned card.
    * if `dealer = True`, heels may be scored; otherwise, nobs may be scored.

* `score_fifteens(Hand)`, `score_pairs(Hand)`, `score_runs(Hand)`
  * each returns a partial score, looking at only one aspect of the hand.

* `check_flush(Hand)`
  * returns `True` if all cards in the hand have the same suit, `False`
    otherwise.

* `value(Card)`
  * returns the point value of the card: 1 for an ace, 10 for an honor, and
    face value for anything else.


### example

```
>>> import cards
>>> deck = cards.make_deck(shuffle = True)
>>> hand = deck.deal(4)
>>> print hand
9d 84h Js
>>> turned = deck.pop()
>>> print turned
9s
>>> 
>>> import cribbage
>>> cribbage.score_hand(hand, turned = turned)
{'nobs': 1, 'pairs': 2}
```

___
I wrote this because I wanted to know what the cribbage score for a whole deck
of cards was. Here's the answer, if you're curious:

```
relsqui@barrett:~/cribbage-scorer$ cat score_the_deck.py 
#!/usr/bin/python

import cards, cribbage

score = cribbage.score_hand(cards.make_deck())
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
