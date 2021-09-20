import threading
from random import randint


ARRAY_LENGTH = THREAD_COUNT = 100

# array to be sorted
numbers = [randint(1, 1000) for _ in range(ARRAY_LENGTH)]


barrier = threading.Barrier(THREAD_COUNT)
mutex = threading.Semaphore(1)
threads_at_barrier = 0
odd_swap = even_swap = False
is_sorted = False


def sort(id):
    global numbers, barrier, mutex, threads_at_barrier, odd_swap, even_swap, is_sorted

    for round_number in range(ARRAY_LENGTH):
        if is_sorted:
            return

        # odd rounds
        if id != ARRAY_LENGTH - 1 and id % 2 == 1 and round_number % 2 == 1:

            if numbers[id] > numbers[id + 1]:
                # swap
                numbers[id], numbers[id +
                                     1] = numbers[id + 1], numbers[id]
                odd_swap = True

        # even rounds
        elif id % 2 == 0 and round_number % 2 == 0:
            if numbers[id] > numbers[id + 1]:
                # swap
                numbers[id], numbers[id +
                                     1] = numbers[id + 1], numbers[id]
                even_swap = True

        with mutex:
            threads_at_barrier += 1
            """
            Last thread in each round always checks if there were any swaps
            in the last two consecutive rounds
            If there were no swaps, the array is sorted
            """
            if threads_at_barrier == THREAD_COUNT:
                if odd_swap == False and even_swap == False:
                    print("Sorted after {} rounds".format(round_number + 1))
                    is_sorted = True
                threads_at_barrier = 0
                odd_swap = even_swap = False

        barrier.wait()


threads = [threading.Thread(target=sort, args=(thread_id,))
           for thread_id in range(ARRAY_LENGTH)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(numbers)