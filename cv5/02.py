import threading
from random import randint

THREAD_COUNT = 20
BUFFER_SIZE = 20

buffer_access = threading.Semaphore(1)
items = threading.Semaphore(0)
buffer_space = threading.Semaphore(BUFFER_SIZE)

buffer = []


def produce():
    global buffer

    while True:
        buffer_space.acquire()
        buffer_access.acquire()

        buffer.append(randint(0, 1000))

        buffer_access.release()
        items.release()


def consume():
    global buffer

    while True:
        items.acquire()
        buffer_access.acquire()

        i = buffer.pop()
        print(i)

        buffer_space.release()
        buffer_access.release()


threads = []

for i in range(THREAD_COUNT):
    threads.append(threading.Thread(target=produce))
    threads.append(threading.Thread(target=consume))

for t in threads:
    t.start()

for t in threads:
    t.join()
