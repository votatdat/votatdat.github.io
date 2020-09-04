class Shape:
    def __init__(self, name):
        self.name = name

    def info(self):
        return f'Shape.info called for Shape({self.name})'

    def extended_info(self):
        return f'Shape.extended_info called for Shape({self.name})', self.info()


class Polygon(Shape):
    def __init__(self, name):
        self.name = name  # we'll come back to this later in the context of using the super()

    def info(self):
        return f'Polygon info called for Polygon({self.name})'
