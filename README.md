## pydeck

is a library for writing card games in python. Basic usage is simple:

```
>>> from pydeck.standard import make_deck
>>>
>>> deck = make_deck(shuffle=True)
>>> hand = deck.deal(5)
>>> print hand
AJ6s 2h 3c
>>> print hand[0]
Ace of Spades
```

The cribbage module implements some example game logic using pydeck.

```
>>> from pydeck.standard import make_deck
>>> from pydeck.cribbage import score_hand
>>>
>>> deck = make_deck(shuffle=True)
>>> hand = deck.deal(4)
>>> turned = deck.pop()
>>> print hand
Jh 8d QTc
>>> print turned
Six of Spades
>>> score_hand(hand, turned)
{'runs': 3, 'fifteens': 0, 'pairs': 0, 'nobs': 0, 'flush': 0, 'heels': 0}
```

### package summary

#### base
base is for abstract classes which can be used on their own in
simple projects or subclassed to build more complex mechanics.

A `CardProperty` is a category a card can belong to, like "spade"
or "three" or "green" or "flying." This base class only has a name;
subclass it to add other attributes, or just to have a new type
for easy comparison.

`Card` is a placeholder which provides a basic equality test to
its subclasses.

`Hand` is a container for storing cards. It behaves like a list in
that it can be indexed or sliced, and implements the standard list
methods as well as these:
* `.shuffle()` is the opposite of `.sort()`, and works in-place.
* `.deal(n)` removes the number of cards you specify and returns them
  as a new `Hand`.


#### standard
standard implements the standard 52-card deck. It defines `Rank`
and `Suit` as card properties, and a list of each: `RANKS` and
`SUITS`. These lists define the sorting order for cards with those
properties. Specific ranks and suits can also be accessed as
constants--`TWO`, `QUEEN`, `HEART`, and so on.

`StandardCard` is your normal playing card. It has a rank, a suit, and
a name.

`StandardHand` is what you hold StandardCards in. To Hand it adds a
tidy string representation (as seen in the examples), and two more
methods:
 * `.by_rank(Rank)` returns a new StandardHand containing the cards
   from your hand which have the given rank. It does *not* remove them
   from your hand.
 * `.by_suit(Suit)` is the same thing but for suits.

Additionally, standard defines some top-level functions.

`make_deck()` creates a full deck of cards, defined as one of
each possible pair of the members of RANKS and SUITS. By default, it is
returned still in order; pass `shuffle=True` to have it shuffled first.

`find_sets()`, `find_flushes()`, and `find_straights()` all take a
StandardHand and return a list of subhands which are of like rank
(sets) or suit (flushes), or of consecutive rank (straights). An
optional `minimum` argument specifies how small a subhand will be
returned; the default is 2 for sets and 1 for the others.


#### cribbage
cribbage implements the hand-scoring rules of cribbage. Its main
interface is `score_hand()`, which takes a StandardHand and returns a
dictionary of ("score-type": points) pairs. You can also pass it
`turned=StandardCard` and the boolean arguments `crib` and `dealer` to
cover all the scoring possibilities.

score_hand() has a series of helper functions which can be called
individually with a StandardHand: `score_fifteens()` etc. return
integers, and `check_flush()` returns a boolean. It also has the
`value()` function, which takes a StandardCard and returns the point
value of that card (for fifteens and the play).

#### poker
poker implements some hand-analyzing tools for poker-type games.

`best_sets()`, `best_flushes()`, and `best_straights()` wrap the
standard module's find functions, returning only the subhands which are
tied for best (longest or highest rank); `find_straight_flushes()` does
what it says. All of these only return subhands with a length of at
least 5.

`find_full_houses()` and `best_full_houses()` are also provided; "best"
in that case is defined by the rank of the triple followed by the rank
of the pair.

___

I originally wrote this because I wanted to know what the cribbage
score for a whole deck of cards was. Now I can find out!

```
>>> from pydeck import standard, cribbage
>>>
>>> def score_deck():
...     score = cribbage.score_hand(standard.make_deck())
...     for key, value in score.items():
...             if value:
...                 print "{} for {:,}".format(key, value)
...     print "total: {:,}".format(sum(score.values()))
... 
>>> score_deck()
runs for 872,415,232
fifteens for 34,528
pairs for 156
total: 872,449,916
```

Plus 1-2 for heels/nobs, depending on the turned card and whether you're
dealing.
