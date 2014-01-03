#!/usr/bin/python

import random, UserList


class EqualityMixin (object):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class CardProperty (EqualityMixin):
    def __init__(self, name, plural = None, short = None):
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
        return "<CardProperty:{}>".format(self.name)


class Hand (UserList.UserList):
    def __repr__(self):
        return "<Hand({}):{}>".format(len(self), ",".join(map(str, self)))

    def shuffle(self):
        random.shuffle(self)

    def deal(self, count):
        if count > len(self):
            raise IndexError("Not enough cards in Hand")
        dealt = self[:count]
        del self[:count]
        return dealt
