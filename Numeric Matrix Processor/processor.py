import copy
import math
import sys

num_to_word = {
    0: 'first',
    1: 'second'
}


def matrix_addition() -> list:
    """
    Adds two matrices.

    Returns:
        list: Matrix in the form of a 2d list
    """
    matrices = []
    rows, cols = 0, 0
    for i in range(2):
        matrix = []
        rows, cols = [int(i) for i in input(f"Enter size of {num_to_word[i]} matrix: ").split()]
        print(f"Enter {num_to_word[i]} matrix")
        for row in range(rows):
            matrix_row = []
            rows_val = input()
            for val in rows_val.split():
                if "." in val:
                    matrix_row.append(float(val))
                else:
                    matrix_row.append(int(val))
            matrix.append(matrix_row)
        matrices.append(matrix)

    # check if matrices can be added
    for matrix in matrices:
        if len(matrix) != rows or len(matrix[0]) != cols:
            return []

    sol_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for matrix in matrices:
        for row in range(rows):
            for col in range(cols):
                sol_matrix[row][col] += matrix[row][col]
    return sol_matrix


def scalar_multiplication() -> list:
    """
    Scalar multiplication of a real number and a matrix

    Returns:
        list: Matrix in the form of 2d list

    """
    rows, cols = [int(e) for e in input(f"Enter size of matrix: ").split()]
    sol_matrix = []
    print("Enter matrix:")
    for row in range(rows):
        matrix_row = []
        rows_val = input()
        for val in rows_val.split():
            if "." in val:
                matrix_row.append(float(val))
            else:
                matrix_row.append(int(val))
        sol_matrix.append(matrix_row)
    num = input("Enter constant: ")
    if "." in num:
        num = float(num)
    else:
        num = int(num)

    for row in range(rows):
        for col in range(cols):
            sol_matrix[row][col] = sol_matrix[row][col] * num

    return sol_matrix


def matrix_multiplication() -> list:
    """
    Matrix multiplication of two matrices

    Returns:
        list: matrix in the form of 2d list
    """
    matrices = []
    matrix2_cols = []

    for i in range(2):
        matrix = []
        rows, cols = [int(i) for i in input(f"Enter size {num_to_word[i]} of matrix: ").split()]
        print(f"Enter {num_to_word[i]} matrix")
        # initialize matrix2_cols
        if i == 1:
            matrix2_cols = [[0 for _ in range(rows)] for _ in range(cols)]
        for row in range(rows):
            matrix_row = []
            rows_val = input()
            if cols != len(rows_val.split()):
                return []

            for val in rows_val.split():
                if "." in val:
                    matrix_row.append(float(val))
                else:
                    matrix_row.append(int(val))
            # keep track of matrix 2 column for multiplication later
            if i == 1:
                for index, val in enumerate(matrix_row):
                    matrix2_cols[index][row] = val
            matrix.append(matrix_row)
        matrices.append(matrix)
    # check if matrices can be multiplied
    if len(matrices[0][0]) != len(matrices[1]):
        return []

    row1, col1 = len(matrices[0]), len(matrices[0][0])
    row2, col2 = len(matrices[1]), len(matrices[1][0])

    sol_matrix = [[0 for _ in range(col2)] for _ in range(row1)]

    for row in range(row1):
        for col in range(col2):
            sol_matrix[row][col] = vector_multiplication(matrices[0][row], matrix2_cols[col])
    return sol_matrix


def vector_multiplication(v1: list, v2: list) -> int:
    """
    Gives product of row matrix and column matrix

    Args:
        v1: row of matrix 1 (row vector)
        v2: column of matrix 2 (column vector)

    Returns:
        int: matrix multiplication of v1 and v2

    """
    if len(v1) != len(v2):
        raise Exception("Different length vectors")
    sol = 0
    for i in range(len(v1)):
        sol += v1[i] * v2[i]
    return sol


def transpose_matrix():
    """
    Gives transpose of the given matrix

    Returns:
        list: Transposed matrix in 2d list form
    """
    option_dict = {
        1: "main_diagonal",
        2: "side_diagonal",
        3: "vertical_line",
        4: "horizontal_line"
    }

    print("1. Main diagonal\n"
          "2. Side diagonal\n"
          "3. Vertical line\n"
          "4. Horizontal line")
    option = int(input())
    rows, cols = [int(e) for e in input(f"Enter size of matrix: ").split()]
    input_matrix = []
    # Matrix that hold columns
    print("Enter matrix:")
    for row in range(rows):
        matrix_row = []
        rows_val = input()
        for val in rows_val.split():
            if "." in val:
                matrix_row.append(float(val))
            else:
                matrix_row.append(int(val))
        input_matrix.append(matrix_row)

    return get_transpose(input_matrix, option_dict[option])


def get_transpose(input_matrix: list, transpose_along: str = "main_diagonal") -> list:
    """
    Calculates transpose of a matrix

    Args:
        input_matrix: Matrix whose transpose needs to be determined
        transpose_along: transpose along what line

    Returns:
        transposed matrix
    """
    rows, cols = len(input_matrix), len(input_matrix[0])
    cols_matrix = [[0 for _ in range(rows)] for _ in range(cols)]
    sol_matrix = None

    for row_i in range(rows):
        for col_i in range(cols):
            cols_matrix[col_i][row_i] = input_matrix[row_i][col_i]

    if transpose_along == "main_diagonal":
        # Transpose along main diagonal
        sol_matrix = cols_matrix
    elif transpose_along == "side_diagonal":
        # Transpose along side diagonal
        for i in range(cols):
            cols_matrix[i].reverse()
        cols_matrix.reverse()
        sol_matrix = cols_matrix
    elif transpose_along == "vertical_line":
        # Transpose along the vertical line
        for i in range(rows):
            input_matrix[i].reverse()
        sol_matrix = input_matrix
    elif transpose_along == "horizontal_line":
        # Transpose along the horizontal line
        input_matrix.reverse()
        sol_matrix = input_matrix

    return sol_matrix


def get_inverse() -> list:
    """
       Gets input for matrix and determines it's inverse if it exists

       Returns:
           int: Inverse of the matrix
    """
    rows, cols = [int(e) for e in input(f"Enter size of matrix: ").split()]
    input_matrix = []

    if rows == cols:
        print("Enter matrix:")
        for row in range(rows):
            matrix_row = []
            rows_val = input()
            for val in rows_val.split():
                if "." in val:
                    matrix_row.append(float(val))
                else:
                    matrix_row.append(int(val))
            input_matrix.append(matrix_row)

    det = calculate_determinant(input_matrix)
    if det is None or det == 0:
        return []

    matrix_of_minors = [[0 for _ in range(rows)] for _ in range(cols)]
    matrix_of_cofactors = [[0 for _ in range(rows)] for _ in range(cols)]

    # Calculate Matrix of Minors
    # Calculate Matrix of Cofactors
    # Calculate Adjugate
    # Multiply by 1/determinate
    for row_i in range(len(input_matrix)):
        for col_i in range(len(input_matrix[0])):
            matrix_of_minors[row_i][col_i] = calculate_determinant(matrix_reducer(input_matrix, col_i, row_i))
            matrix_of_cofactors[row_i][col_i] = math.pow(-1, row_i+col_i) * matrix_of_minors[row_i][col_i]

    transposed_matrix = get_transpose(matrix_of_cofactors)

    for row_i in range(len(transposed_matrix)):
        for col_i in range(len(transposed_matrix[0])):
            transposed_matrix[row_i][col_i] = (1 / det) * transposed_matrix[row_i][col_i]

    return transposed_matrix


def get_determinant() -> int:
    """
    Gets input for matrix and determines it's determinant

    Returns:
        int: determinant of the input matrix
    """
    rows, cols = [int(e) for e in input(f"Enter size of matrix: ").split()]
    input_matrix = []
    determinant = None

    if rows == cols:
        print("Enter matrix:")
        for row in range(rows):
            matrix_row = []
            rows_val = input()
            for val in rows_val.split():
                if "." in val:
                    matrix_row.append(float(val))
                else:
                    matrix_row.append(int(val))
            input_matrix.append(matrix_row)
        if rows == 1:
            return input_matrix[0][0]
        determinant = calculate_determinant(input_matrix)
    return determinant


def calculate_determinant(input_matrix: list, determinant=0) -> int:
    """
    Calculates determinant of the given square matrix
    Args:
        input_matrix: matrix in list form
        determinant: current determinant, required for recursion

    Returns:
        int: determinant of the input matrix
    """
    if len(input_matrix) == 2:
        return input_matrix[0][0] * input_matrix[1][1] - input_matrix[0][1] * input_matrix[1][0]

    for i in range(len(input_matrix[0])):
        r, c = 1, i + 1
        determinant += input_matrix[0][i] * math.pow(-1, r + c) * calculate_determinant(matrix_reducer(input_matrix, i))

    return determinant


def matrix_reducer(input_matrix: list, col_i: int, row_i: int = 0) -> list:
    """
    Helper function to calculate determinant. Removes col_i'th column and row_i'th row.

    Args:
        input_matrix: matrix in list form
        col_i: column to remove
        row_i: row to remove, by default 0

    Returns:
        list: matrix whose remove_index'th row and column is removed

    Example:
        input_matrix = [[1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 1],
                        [2, 3, 4, 5, 6],
                        [7, 8, 9, 1, 2],
                        [3, 4, 5, 6, 7]]
        remove_index = 1

        return_matrix = [[6, 8, 9, 1],
                         [2, 4, 5, 6],
                         [7, 9, 1, 2],
                         [3, 5, 6, 7]]
    """
    matrix = copy.deepcopy(input_matrix)
    matrix.pop(row_i)
    for row in matrix:
        row.pop(col_i)

    return matrix


def read_matrix(n=1):
    """
    TODO
    Reads matrix from terminal

    Args:
        n: number of matrices

    Returns:
        list: list of matrices
    """
    pass


def exit_program():
    """
    Exits program

    Returns:
        None
    """
    sys.exit(0)


def main():
    """
    Main entry point.

    Returns:
        None

    """
    func_dict = {
        1: matrix_addition,
        2: scalar_multiplication,
        3: matrix_multiplication,
        4: transpose_matrix,
        5: get_determinant,
        6: get_inverse,
        0: exit_program
    }

    while True:
        print("1. Add matrices\n"
              "2. Multiply matrix by a constant\n"
              "3. Multiply matrices\n"
              "4. Transpose matrix\n"
              "5. Calculate a determinant\n"
              "6: Inverse matrix\n"
              "0. Exit"
              )
        option = int(input("Your choice: "))
        # print solution
        solution = func_dict[option]()
        if type(solution) == list:
            if len(solution) == 0:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                for row in solution:
                    print(str(' '.join(str(e) for e in row)))
        else:
            if solution is None:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                print(solution)
        print()


if __name__ == '__main__':
    main()
