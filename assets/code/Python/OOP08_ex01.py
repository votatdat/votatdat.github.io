class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person('{self.name}')"


class Family:
    def __init__(self, mother, father):
        self.mother = mother
        self.father = father
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self
