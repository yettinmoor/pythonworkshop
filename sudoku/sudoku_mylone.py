#! python3

VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def get_matrix(path):
    """Used by both solutions"""
    with open(path) as file:
        matrix = [list(line.strip()) for line in file.readlines()]
    matrix = [[int(matrix[row][col]) for col in range(len(matrix[0]))] for row in range(len(matrix))]
    return matrix


def get_nums_in_row(matrix, row):
    """Returns a list of all items in the given row."""
    return matrix[row]


def get_nums_in_col(matrix, col):
    """Returns a list of all items in the given col."""
    return [matrix[row_][col] for row_ in range(len(matrix))]


def get_nums_in_square(matrix, row, col):
    """Returns all items in the 3x3 square for the given row and col as a flat list."""
    return [matrix[row_][col_] for row_ in range((row // 3) * 3, ((row // 3) * 3) + 3) for col_ in range((col // 3) * 3, ((col // 3) * 3) + 3)]


def prep_empty_cells(matrix, symbol):
    """Replace all instances of the given symbol in the matrix with an empty list."""
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == symbol:
                matrix[row][col] = []


def get_possible_nums(matrix, row, col):
    nums_in_pos = VALUES
    for val in VALUES:
        if (val in get_nums_in_row(matrix, row)
            or val in get_nums_in_col(matrix, col)
            or val in get_nums_in_square(matrix, row, col)) and val in nums_in_pos:
            nums_in_pos.remove(val)
    return nums_in_pos


def fill_possible_nums(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if type(matrix[row][col]) is list:
                    new_value = get_possible_nums(matrix, row, col)
                    if new_value != matrix[row][col]:
                        matrix[row][col] = new_value
                        changed = True
    return changed


def convert_singles(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if type(matrix[row][col]) is list:
                if len(matrix[row][col]) == 1:
                    matrix[row][col] = matrix[row][col][0]
                    changed = True
    return changed


def convert_unique_in_row(matrix):
    changed = False
    for row in range(len(matrix)):
        uniques = get_uniques(matrix[row])
        for item in uniques:
            matrix[row][item[1]] = item[0]
            changed = True
    return changed


def convert_unique_in_col(matrix):
    changed = False
    for col in range(len(matrix[0])):
        uniques = get_uniques(get_nums_in_col(matrix, col))
        for item in uniques:
            matrix[item[1]][col] = item[0]
            changed = True
    return changed


def convert_unique_in_square(matrix):
    changed = False
    for row in range(0, len(matrix), 3):
        for col in range(0, len(matrix[0]), 3):
            uniques = get_uniques(get_nums_in_square(matrix, row, col))
            for item in uniques:
                matrix[(3 * (row // 3)) + (item[1] // 3)][(3 * (col // 3)) + (item[1] % 3)] = item[0]
                changed = True
    return changed


def get_uniques(list_):
    uniques = []
    for val in VALUES:
        indices = []
        for i in range(len(list_)):
            if type(list_[i]) is list and val in list_[i]:
                indices.append(i)
        if len(indices) == 1:
            uniques.append((val, indices[0]))
    return uniques


def is_solved(matrix):
    solved = True
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if type(matrix[row][col]) is list:
                solved = False
    return solved


def get_shortest_possible(matrix, exlude=[]):
    index = None
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if type(matrix[row][col]) is list:
                if index is None and (row, col) not in exlude:
                    index = (row, col)
                elif (row, col) not in exlude:
                    if len(matrix[row][col]) < len(matrix[index[0]][index[1]]):
                        index = (row, col)
    return index


def solve(matrix):
    while not is_solved(matrix):
        changed = (
            fill_possible_nums(matrix)
            or convert_singles(matrix)
            or convert_unique_in_row(matrix)
            or convert_unique_in_col(matrix)
            or convert_unique_in_square(matrix)
            )

        if not changed:
            tested_indices = []
            index = False

            while index is False or index in tested_indices:
                index = get_shortest_possible(matrix, tested_indices)

            if index is None:
                return matrix

            tested_indices.append(index)
            for item in matrix[index[0]][index[1]]:
                test_matrix = matrix[:][:]
                test_matrix[index[0]][index[1]] = item
                solve(test_matrix)
                if is_solved(test_matrix):
                    matrix = test_matrix
                    break
    return matrix


def solve_sudoku(path):
    """My and Lone's solution."""
    matrix = get_matrix(path)
    prep_empty_cells(matrix, 0)

    return solve(matrix)

# path = r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_extreme.txt'

# solved_matrix = solve_sudoku(path)
# for row in solved_matrix:
#     print(row)
