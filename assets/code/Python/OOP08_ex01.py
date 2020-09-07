class IntegerValue:
    def get(self):
        return self._value

    def set(self, value):
        self._value = int(value)

    def __init__(self, value=None):
        if value:
            self.set(value)


class Point2D:
    x = IntegerValue()
    y = IntegerValue()
