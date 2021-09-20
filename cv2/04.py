import threading

matrix_a = [[1, 2, 3],
            [4, 5, 6]]

matrix_b = [[1, 2],
            [3, 4],
            [5, 6]]

matrix_c = [[1, 2],
            [3, 4]]

matrix_d = [[5, 6],
            [7, 8]]


def print_matrix(matrix):
    for row in matrix:
        print(row)


def matrix_dot_product(a, row, b, col, result):
    # go through elements in b's column
    b_row = 0
    for i in a[row]:
        result[row][col] += i * b[b_row][col]
        b_row += 1


def matrix_multiplication(a, b):
    # Expecting matrices are input correctly, only checking
    # if multiplication is possible
    if not len(a[0]) == len(b):
        raise ValueError("Incorrent matrix dimensions")

    # Create 'result' matrix with correct dimensions
    result_rows = len(a)
    result_cols = len(b[0])
    result = [[0 for x in range(result_rows)] for x in range(result_cols)]

    # Create a thread for each cell in 'result' matrix that calculates the corresponding value
    threads = []
    for row in range(result_rows):
        for col in range(result_cols):
            threads.append(threading.Thread(
                target=matrix_dot_product, args=(a, row, b, col, result,)))

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    return result


a_times_b = matrix_multiplication(matrix_a, matrix_b)
c_times_d = matrix_multiplication(matrix_c, matrix_d)

print_matrix(a_times_b)
print()
print_matrix(c_times_d)