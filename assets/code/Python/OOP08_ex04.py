from random import choice, seed


class Choice:
    def __init__(self, *choices):
        self.choices = choices

    def __get__(self, instance, owner_class):
        return choice(self.choices)


class Deck:
    suit = Choice('Spade', 'Heart', 'Diamond', 'Club')
    card = Choice(*'23456789JQKA', '10')
