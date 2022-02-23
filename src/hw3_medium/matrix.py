from numpy.lib.mixins import NDArrayOperatorsMixin
import numpy as np


class InvalidArgumentError(Exception):
    pass


class MyMixin:
    def __init__(self, state):
        cols = len(state[0]) if len(state) > 0 else 0
        for row in state:
            if cols != len(row):
                raise InvalidArgumentError

        self.__state = state
        self.__rows = len(self.state) if cols > 0 else 0
        self.__cols = cols
        self.__shape = (self.rows, self.cols)

    @staticmethod
    def zeros(i, j):
        return Matrix([[0] * j for _ in range(i)])

    @property
    def state(self):
        return self.__state

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def shape(self):
        return self.__shape

    def __getitem__(self, key):
        return self.__state[key]

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, MyMixin):
                return NotImplemented

        inputs = tuple(x.state if isinstance(x, MyMixin) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.state if isinstance(x, MyMixin) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.state)

    def __str__(self):
        return self.__repr__()

    def write_to_file(self, filename):
        with(open(filename, "w")) as out:
            out.write(str(self))


class Matrix(NDArrayOperatorsMixin, MyMixin):
    pass


if __name__ == '__main__':
    import numpy as np

    np.random.seed(0)
    m1 = Matrix(np.random.randint(0, 10, (10, 10)))
    m2 = Matrix(np.random.randint(0, 10, (10, 10)))

    (m1 + m2).write_to_file("artifacts/matrix+.txt")
    (m1 - m2).write_to_file("artifacts/matrix-.txt")
    (m1 * m2).write_to_file("artifacts/matrix*.txt")
    (m1 @ m2).write_to_file("artifacts/matrix@.txt")
