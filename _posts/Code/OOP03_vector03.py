from numbers import Real


class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(
                    f'Vector components must all be real numbers - {component} is invalid.')

        # use immutable storage for vector
        self._components = tuple(components)

    def __len__(self):
        return len(self._components)

    @property
    def components(self):
        return self._components

    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'

    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)

    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)

    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)

    def __mul__(self, other):
        print('__mul__ called...')
        if not isinstance(other, Real):
            return NotImplemented
        components = (other * x for x in self.components)
        return Vector(*components)

    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
