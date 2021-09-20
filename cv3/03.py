import threading
from random import randint
from math import gcd

# Buffer for generated pairs
pair_buffer = []

# Buffer to store result about commensurability
result_buffer = -1

ones_count = 0
pairs_count = 0

# Stop after reading this amount of 1's
max_ones = 5000
max_ones_reached = False

# The interval random numbers get generated in
random_interval = [0, 10000]

sem_generate = threading.Semaphore(1)
sem_check = threading.Semaphore(0)
sem_write_result = threading.Semaphore(1)
sem_read_result = threading.Semaphore(0)


def is_commensurable(num1, num2):
    if(gcd(num1, num2) > 1):
        return 1
    else:
        return 0


def generate():
    global pair_buffer, random_interval
    while(True):
        if(max_ones_reached):
            return 1

        sem_generate.acquire()

        for i in range(2):
            pair_buffer.append(
                randint(random_interval[0], random_interval[1]))
        # print("GENERATED: {}".format(number_buffer))

        sem_check.release()


def check_commensurability():
    global result_buffer
    while(True):
        if(max_ones_reached):
            return 1

        sem_write_result.acquire()
        sem_check.acquire()

        num1 = pair_buffer.pop()
        num2 = pair_buffer.pop()
        result_buffer = is_commensurable(num1, num2)
        # print("READ FROM NUMBER BUFFER: {}, {}, RESULT: {}".format(
        #     num1, num2, result_buffer))

        sem_generate.release()
        sem_read_result.release()


def count_results():
    global pairs_count, ones_count, result_buffer, max_ones_reached
    while(True):
        sem_read_result.acquire()

        pairs_count += 1
        if(result_buffer == 1):
            ones_count += 1
        # print("READ RESULT: {}, zeros count: {}, ones count: {}".format(
        #     result_buffer, zeros_count, ones_count))

        if(ones_count == max_ones):
            max_ones_reached = True
            # release all semaphores to prevent deadlock
            sem_generate.release()
            sem_write_result.release()
            sem_check.release()
            return 0

        sem_write_result.release()


threads = []

threads.append(threading.Thread(target=generate))
threads.append(threading.Thread(target=check_commensurability))
threads.append(threading.Thread(target=count_results))

for t in threads:
    t.start()

for t in threads:
    t.join()

print("DONE")
print("Generated pairs: {}, Commensurable: {}, Incommensurable: {}".format(
    pairs_count, ones_count, pairs_count-ones_count))