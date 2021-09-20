A = [[1, 2],
     [3, 4]]

B = [[1, 2],
     [3, 4]]

matrix_size = len(A)

A_line = A[0]

result_line = [0 for _ in range(matrix_size)]

for result_idx in range(matrix_size):
    B_idx = 0
    for i in A_line:
        result_line[result_idx] += i * B[B_idx][result_idx]
        B_idx += 1
    



C = []
C.append(result_line)

print(C)
