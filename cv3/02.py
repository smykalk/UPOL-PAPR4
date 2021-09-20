import threading
from random import randint
from math import gcd

# Buffer for generated doubles
number_buffer = []

# Buffer to store result about commensurability
result_buffer = -1

ones_count = 0
zeros_count = 0

# The interval random numbers get generated in
random_interval = [0, 1000]

generate = threading.Semaphore(1)
check = threading.Semaphore(0)
write_result = threading.Semaphore(1)
read_result = threading.Semaphore(0)


def is_commensurable(num1, num2):
    if(gcd(num1, num2) > 1):
        return 1
    else:
        return 0


def produce():
    global number_buffer, random_interval
    while(True):
        generate.acquire()
        for i in range(2):
            number_buffer.append(randint(random_interval[0],random_interval[1]))
        print("GENERATED: {}".format(number_buffer))
        check.release()


def check_commensurability():
    global result_buffer
    while(True):
        write_result.acquire()
        check.acquire()
        num1 = number_buffer.pop()
        num2 = number_buffer.pop()
        result_buffer = is_commensurable(num1, num2)
        print("READ FROM NUMBER BUFFER: {}, {}, RESULT: {}".format(
            num1, num2, result_buffer))
        generate.release()
        read_result.release()


def count_results():
    global zeros_count, ones_count, result_buffer
    while(True):
        read_result.acquire()
        if(result_buffer == 1):
            ones_count += 1
        else:
            zeros_count += 1
        print("READ RESULT: {}, zeros count: {}, ones count: {}".format(
            result_buffer, zeros_count, ones_count))
        write_result.release()


threads = []

threads.append(threading.Thread(target=produce))
threads.append(threading.Thread(target=check_commensurability))
threads.append(threading.Thread(target=count_results))

for t in threads:
    t.start()

for t in threads:
    t.join()
