import unittest
from matrix import Matrix

cases = [
    [[]],
    [[1]],
    [[1], [2]],
    [[1, 2]],
    [[1, 2], [3, 4]],
    [[1, 2, 3], [4, 5, 6]],
    [[1, 2], [3, 4], [5, 6]],
    [[1, 2, 3, 4, 5, 6]],
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
]


class MatrixTest(unittest.TestCase):
    def test_zeros(self):
        l1, l2 = 4, 4
        m = Matrix.zeros(l1, l2)
        self.assertEqual(m.rows, l1)
        self.assertEqual(m.cols, l2)
        for i in range(l1):
            for j in range(l2):
                self.assertEqual(m[i][j], 0)

    def test_add(self):
        for case in cases:
            double = Matrix([[2 * x for x in row] for row in case])
            self.assertEqual(Matrix(case) + Matrix(case), double)

    def test_sub(self):
        for case in cases:
            c = Matrix(case)
            self.assertEqual(c - c, Matrix.zeros(*c.shape))

    def test_mul(self):
        for case in cases:
            double = Matrix([[x * x for x in row] for row in case])
            self.assertEqual(Matrix(case) * Matrix(case), double)

    def test_matmul(self):
        empty = Matrix(cases[0])
        self.assertEqual(empty @ empty, empty)
        one = Matrix(cases[1])
        self.assertEqual(one @ one, one)
        self.assertEqual(Matrix(cases[3]) @ Matrix(cases[2]), Matrix([[5]]))
        self.assertEqual(Matrix(cases[3]) @ Matrix(cases[4]), Matrix([[7, 10]]))
        self.assertEqual(Matrix(cases[4]) @ Matrix(cases[2]), Matrix([[5], [11]]))
        self.assertEqual(Matrix(cases[4]) @ Matrix(cases[5]), Matrix([[9, 12, 15], [19, 26, 33]]))
        self.assertEqual(Matrix(cases[8]) @ Matrix(cases[6]), Matrix([[22, 28], [49, 64], [76, 100]]))
