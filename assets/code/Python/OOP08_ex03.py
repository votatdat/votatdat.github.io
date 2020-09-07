from random import choice, seed


class Deck:
    @property
    def suit(self):
        return choice(('Spade', 'Heart', 'Diamond', 'Club'))

    @property
    def card(self):
        return choice(tuple('23456789JQKA') + ('10',))
