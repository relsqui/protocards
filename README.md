## cribbage-scorer

Some basic card classes and a cribbage scoring library.


#### cards.py

###### constants
* `RANKS` = "23456789TJQKA"
* `SUITS` = "cdhs"
* dictionaries `RANK_NAMES` and `SUIT_NAMES` map the above to titlecased words.
* override these to change the deck type, or reorder rank and suit values.
  * any new ranks or suits should be added to `RANK_NAMES` and `SUIT_NAMES`.
  * non-unique characters in `RANKS` and `SUITS` aren't supported and may
    cause unusual behavior.

###### classes
* `Card(string)`
  * initialize with a rank + suit string, e.g "Jh" for the Jack of Hearts.
    * invalid rank + suit strings raise `ValueError`.
  * no exposed methods.
  * can be compared and sorted; will use rank first, then suit, as ordered
    in the constant strings.

* `Hand(Card, ...)`
    * raises `TypeError` if something other than a `Card` is added, either at
      initialization or later.
  * `.append(Card)` or `.extend([Card, ...])` to add cards.
  * `.sort()` or `.shuffle()` in place.
  * `.pop()` or `.deal(count)` to remove and return members.
  * view subsets `.by_rank(rank)` or `.by_suit(suit)`.
    * raises `ValueError` if rank not in `RANKS` or suit not in `SUITS`.

###### functions
* `make_deck(shuffle = True)`
   * returns a `Hand` populated with one of every unique card possible given
     the values of `RANKS` and `SUITS`.
   * by default, will shuffle the deck; set `shuffle = False` to keep sorted.


#### cribbage.py

###### constants
* overrides `cards.RANKS` to "A23456789TJQK", making aces sort low.

###### functions
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
  * returns True if all cards in the hand have the same suit, False otherwise.

* `value(Card)`
  * returns the point value of the card.

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
