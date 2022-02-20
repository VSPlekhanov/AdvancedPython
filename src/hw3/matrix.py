class InvalidArgumentError(Exception):
    pass


class Matrix:

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

    def __eq__(self, other):
        if self.shape == (0, 0):
            return True
        for i in range(self.rows):
            for j in range(self.cols):
                if not self[i][j] == other[i][j]:
                    return False
        return True

    def __for_each(self, other, bin_op):
        if self.shape != other.shape:
            raise InvalidArgumentError
        if self.shape == (0, 0):
            return self
        res = Matrix.zeros(*self.shape)
        for i in range(self.rows):
            for j in range(self.cols):
                res[i][j] = bin_op(self[i][j], other[i][j])
        return res

    def __add__(self, other):
        return self.__for_each(other, lambda a, b: a + b)

    def __mul__(self, other):
        return self.__for_each(other, lambda a, b: a * b)

    def __sub__(self, other):
        return self.__for_each(other, lambda a, b: a - b)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise InvalidArgumentError
        if self.shape == (0, 0):
            return self
        res = Matrix.zeros(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                val = 0
                for k in range(other.rows):
                    val += self[i][k] * other[k][j]
                res[i][j] = val
        return res

    def __repr__(self):
        return "\n".join(["\t".join([str(x) for x in row]) for row in self.state])


if __name__ == '__main__':
    import numpy as np

    np.random.seed(0)
    m1 = Matrix(np.random.randint(0, 10, (10, 10)))
    m2 = Matrix(np.random.randint(0, 10, (10, 10)))

    with(open("artifacts/matrix+.txt", "w")) as out:
        out.write(str(m1 + m2))

    with(open("artifacts/matrix*.txt", "w")) as out:
        out.write(str(m1 * m2))

    with(open("artifacts/matrix@.txt", "w")) as out:
        out.write(str(m1 @ m2))
