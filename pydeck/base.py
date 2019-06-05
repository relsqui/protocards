"""Provides abstract tools for building card, hand, and game types."""

import random
import collections


class EqualityMixin(object):

    """Provide equality tests based on `__dict__`."""

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other


class CardProperty(EqualityMixin):

    """A property which can be used to define or describe a card.

    `CardProperty` is meant to be subclassed to define more specific
    attributes of a card, or simply categories of card with no data
    associated with them. See `Rank` and `Suit` in `pydeck.standard`.

    Required Argument:
        name   - String; describes the property.

    Optional Arguments:
        plural - String; plural form of the name. Will be set to
                 `name` + "s" if not specified.
        short  - String; short form of the name. Will be set to
                 `name[0]` if not specified.

    The values of all three arguments are provided as attributes.

    """

    def __init__(self, name, plural=None, short=None):
        self.name = name
        if plural is None:
            self.plural = self.name + "s"
        else:
            self.plural = plural
        if short is None:
            self.short = self.name[0]
        else:
            self.short = short

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{}:{}>".format(self.__class__.__name__, self.short)


class Card(EqualityMixin):

    """Placeholder to provide equality tests to subclasses."""

    pass


class Hand(collections.UserList):

    """List-like class for storing and dealing cards.

    `Hand` extends `UserList` and has the behavior and methods of a list
    in addition to those listed below. Initialize optionally with a
    sequence.

    """

    def __repr__(self):
        return "<{}({}):{}>".format(self.__class__.__name__,
                                    len(self), ",".join(map(str, self)))

    def shuffle(self):
        """Shuffle the contents of the hand."""
        random.shuffle(self)

    def deal(self, count):
        """Remove `count` items from the hand and return them.

        Raises IndexError if there are not enough items to remove.

        """
        if count > len(self):
            raise IndexError("Not enough cards in Hand")
        dealt = self.__class__(self[-count:])
        del self[-count:]
        return dealt
