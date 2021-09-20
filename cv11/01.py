from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


def print_matrix(matrix):
    for row in matrix:
        print(row)


if rank == 0:
    A = [[1, 2, 3, 1],
         [4, 5, 6, 2],
         [7, 8, 9, 3],
         [7, 4, 6, 3]]

    B = [[1, 2, 3, 3],
         [4, 5, 6, 2],
         [7, 8, 9, 1],
         [6, 8, 6, 7]]

    matrix_size = len(A)

    for i in range(1, matrix_size):
        # Send each process matrix_size, its corresponding line
        # and the whole B matrix
        comm.send(matrix_size, dest=i, tag=0)
        comm.send(A[i], dest=i, tag=1)
        comm.send(B, dest=i, tag=2)

        # Calculate the first line
        A_line = A[0]

        result_line = [0 for _ in range(matrix_size)]

    for result_idx in range(matrix_size):
        B_idx = 0
        for i in A_line:
            result_line[result_idx] += i * B[B_idx][result_idx]
            B_idx += 1

        C = []
        C.append(result_line)

    # Receive other lines and append them to the result
    for i in range(1, matrix_size):
        C.append(comm.recv(source=i, tag=3))

    print_matrix(C)


if rank > 0:
    matrix_size = comm.recv(source=0, tag=0)
    # Calculate other lines and send them back
    if rank < matrix_size:
        A_line = comm.recv(source=0, tag=1)
        B = comm.recv(source=0, tag=2)

        result_line = [0 for _ in range(matrix_size)]

        for result_idx in range(matrix_size):
            B_idx = 0
            for i in A_line:
                result_line[result_idx] += i * B[B_idx][result_idx]
                B_idx += 1

        comm.send(result_line, dest=0, tag=3)
