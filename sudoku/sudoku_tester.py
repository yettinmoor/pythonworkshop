#! python3

import time

from killable_thread import thread_with_trace

from sudoku_mylone import solve_sudoku as solve_sudoku_ml
from sudoku_mylone import get_nums_in_col, get_nums_in_square


PATHS = {
    'supereasy' : r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_supereasy.txt',
    'easy' : r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_easy.txt',
    'hard' : r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_hard.txt',
    'superhard' : r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_superhard.txt',
    'expert' : r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_expert.txt',
    'extreme' : r'C:\Users\Dator 4\Documents\MyCodes\Python\sudoku_matrix_extreme.txt'
    }

VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def timeout(sec):
    """Timeout decorator."""
    def outer(func):
        def inner(*args, **kwargs):
            result = None
            thread = thread_with_trace(*args, target=func, **kwargs)
            thread.start()
            thread.join(sec)

            if thread.isAlive():
                thread.kill()
                return(f'ERROR: {func.__name__} took too long to execute. Function call was aborted.')
            else:
                result = thread.get_return()
            return result
        return inner
    return outer


def print_matrix(matrix):
    """Prints the matrix to the console, row by row."""
    for row in matrix:
        print(row)


def check_rows(matrix):
    for row in matrix:
        if len(row) is not 9:
            print('row len')
            return False
        for val in VALUES:
            if val not in row:
                print('row vals')
                print(f'VAL: {val}, ROW: {row}')
                return False
    return True


def check_cols(matrix):
    for col in range(9):
        col_vals = get_nums_in_col(matrix, col)
        if len(col_vals) is not 9:
            print('col len')
            return False
        for val in VALUES:
            if val not in col_vals:
                print('col_vals')
                return False
    return True


def check_squares(matrix):
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            square_vals = get_nums_in_square(matrix, row, col)
            if len(square_vals) is not 9:
                print('square len')
                print(square_vals)
                return False
            for val in VALUES:
                if val not in square_vals:
                    print('square_vals')
                    return False
    return True


def checks_out(matrix):
    try:
        return check_rows(matrix) and check_cols(matrix) and check_squares(matrix)
    except TypeError:
        return False


def run_test(func, *args):
    @timeout(2)
    def sudoku_function_test():
        return func(*args)   
    return sudoku_function_test()


def test():
    tab = ' ' * 4
    test_funcs = {
        'My&Lone' : solve_sudoku_ml,
    }

    print(f'>>> Testing sudoku solutions. <<<')
    for name, path in PATHS.items():
        print(f'Test level: {name}')
        for team, func in test_funcs.items():        
            test_result = run_test(func, path)
            checks = checks_out(test_result) if not type(test_result) is str else test_result
            print(f'{tab}Test team: {team}, Checks out: {checks}')


if __name__ == '__main__':
    test()
    input('Press enter to end...')
