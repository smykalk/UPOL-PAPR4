"""
# Globální hodnoty
    integer array[0..9] C # 10 po dvou různých hodnot
    integer array[0..9] D # Obsahuje samé 0
    -----------------------------------------------------
    Proces i = [0..9]:

    integer myNumber, count

    P1: myNumber <- C[i]
    P2: count <- Počet čísel z C menších než myNumber
    P3: D[count] <- myNumber
"""

import threading

C = [10, 2, 13, 5, 6, 3, 16, 22, 4, 0]
D = [0] * 10

def count_lt(n):
    count = 0
    for i in C:
        if i < n:
            count += 1
    return count

def thread_function(i):
    global C
    my_number = C[i]
    count = count_lt(my_number)
    D[count] = my_number


thread = []

for i in range(10):
    thread.append(threading.Thread(target=thread_function, args=(i,)))

for i in range(10):
    thread[i].start()

for i in range(10):
    thread[i].join()


print(D)