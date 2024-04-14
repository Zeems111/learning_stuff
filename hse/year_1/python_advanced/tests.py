import copy


class MatrixSizeError(Exception):
    pass


class Matrix:
    # Part 1
    def __init__(self, matrix):
        if type(matrix[0]) is int:
            self._matrix = [copy.deepcopy(matrix)]
        else:
            self._matrix = copy.deepcopy(matrix)

    @property
    def matrix(self):
        if len(self._matrix) == 1:
            return self._matrix[0]
        else:
            return self._matrix

    def __str__(self) -> str:
        result = ''
        for i in range(len(self._matrix)):
            if i == 0:
                start = ''
            else:
                start = '\n'
            current = '\t'.join(str(x) for x in self._matrix[i])
            result += start + current
        return result

    # Part 2
    def __eq__(self, other) -> bool:
        if type(other) != Matrix:
            raise TypeError
        if self.size() != other.size():
            return False
        is_equal = True
        for i in range(self.size()[0]):
            for j in range(self.size()[1]):
                if self._matrix[i][j] != other._matrix[i][j]:
                    is_equal = False
                    break
        return is_equal

    def size(self) -> tuple:
        rows = len(self._matrix)
        columns = len(self._matrix[0])
        return rows, columns

    # Part 3
    def __add__(self, other) -> "Matrix":
        if type(other) != Matrix:
            raise TypeError
        if self.size() != other.size():
            raise MatrixSizeError
        rows, columns = self.size()
        result = []
        for i in range(rows):
            s = [*map(sum, zip(self._matrix[i], other._matrix[i]))]
            result.append(s)
        return Matrix(result)

    def __sub__(self, other) -> "Matrix":
        if type(other) != Matrix:
            raise TypeError
        if self.size() != other.size():
            raise MatrixSizeError
        rows, columns = self.size()

        result = []
        for i in range(rows):
            s = [*map(lambda x:x[0]-x[1], zip(self._matrix[i], other._matrix[i]))]
            result.append(s)
        return Matrix(result)

    def transpose(self) -> "Matrix":
        rows, columns = self.size()
        result = []
        for i in range(columns):
            result.append([])
            for j in range(rows):
                result[i].append(self._matrix[j][i])
        return Matrix(result)

    # Part 4
    def __mul__(self, other) -> "Matrix":
        if type(other) != Matrix:
            raise TypeError

        self_rows, self_columns = self.size()
        other_rows, other_columns = other.size()
        if self_columns != other_rows:
            raise MatrixSizeError

        tmp = other.transpose()
        result = []
        for i in range(self_rows):
            s = []
            for j in range(other_columns):
                s.append(sum([*map(lambda x:x[0] * x[1], zip(self._matrix[i], tmp._matrix[j]))]))
            result.append(s)

        result = Matrix(result)
        return result

    # Part 6
    def tr(self) -> float:
        rows, columns = self.size()
        if rows != columns:
            raise MatrixSizeError
        return sum([self._matrix[i][i] for i in range(rows)])

    def det(self) -> float:
        m, n = self.size()
        if m != n:
            raise MatrixSizeError
        elif m == 1:
            return self._matrix[0][0]
        d = 0
        for i in range(m):
            a_i = self.matrix[i][0] * (-1 if i % 2 == 1 else 1)
            matr = []
            for j in range(m):
                if j == i:
                    continue
                matr.append(self._matrix[j][1:])
            matr = Matrix(matr)
            d += a_i * matr.det()
        return d



def check():

    matrix_1 = Matrix([[1, 2], [4, 5], [7, 8]])
    matrix_2 = Matrix([[-8, 9, 12], [-7, 5, 6]])
    matrix_3 = Matrix([[-22, 19, 24], [-67, 61, 78], [-112, 103, 132]])
    if matrix_1 * matrix_2 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'

    matrix_3 = Matrix([[112, 125], [55, 59]])
    if matrix_2 * matrix_1 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'

    matrix_1 = Matrix([[6]])
    matrix_2 = Matrix([[7]])
    matrix_3 = Matrix([[42]])
    if matrix_1 * matrix_2 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'
    if matrix_2 * matrix_1 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'

    matrix_1 = Matrix([[-12345]])
    matrix_2 = Matrix([[0]])
    matrix_3 = Matrix([[0]])
    if matrix_1 * matrix_2 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'
    if matrix_2 * matrix_1 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'

    matrix_1 = Matrix([[1, 2], [4, 5], [7, 8], [-9, 0]])
    matrix_2 = Matrix([[-8, 9, 12], [-7, 5, 6]])
    matrix_3 = Matrix([[-22, 19, 24], [-67, 61, 78], [-112, 103, 132], [72, -81, -108]])
    if matrix_1 * matrix_2 != matrix_3:
        return '0\tIncorrect method mul. Please try again!'

    try:
        _ = matrix_2 * matrix_1
        return '0\tIncorrect method mul. Please try again!'
    except MatrixSizeError: print('MatrixSizeError')
    except Exception: return '0\tIncorrect method mul. Please try again!'

    try:
        _ = matrix_1 * 5
        return '0\tIncorrect method mul. Please try again!'
    except TypeError: print('TypeError')
    except Exception: return '0\tIncorrect method mul. Please try again!'

    try:
        _ = matrix_2 * [5, 4, 6, 1]
        return '0\tIncorrect method mul. Please try again!'
    except TypeError: print('TypeError')
    except Exception: return '0\tIncorrect method mul. Please try again!'

    try:
        _ = matrix_3 * {'a': 1, 'b': 2}
        return '0\tIncorrect method mul. Please try again!'
    except TypeError: print('TypeError')
    except Exception: return '0\tIncorrect method mul. Please try again!'

    try:
        _ = Matrix([[-12345]]) * Matrix([[-12345], [-12345]])
        return '0\tIncorrect method mul. Please try again!'
    except MatrixSizeError: print('MatrixSizeError')
    except Exception: return '0\tIncorrect method mul. Please try again!'


    return '1\tGreat job! You passed all test cases.'


result, message = check().split('\t')
assert result == '1', message
print(message)