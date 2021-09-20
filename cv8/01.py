import threading
from random import randint
from math import gcd


def is_commensurable(num1, num2):
    if(gcd(num1, num2) > 1):
        return 1
    else:
        return 0


class CommCounter:
    random_interval = [0, 1000]

    def __init__(self):
        self.number_buffer = []
        self.result_buffer = []
        self.ones_count = 0
        self.zeros_count = 0

        self.produce_consume_lock = threading.Lock()
        self.read_write_result_lock = threading.Lock()

        self.number_buffer_empty = threading.Condition(
            self.produce_consume_lock)
        self.number_buffer_full = threading.Condition(
            self.produce_consume_lock)

        self.result_buffer_empty = threading.Condition(
            self.read_write_result_lock)
        self.result_buffer_full = threading.Condition(
            self.read_write_result_lock)

    def produce(self):
        while True:
            with self.produce_consume_lock:
                while self.number_buffer:
                    self.number_buffer_empty.wait()

                for _ in range(2):
                    self.number_buffer.append(
                        randint(self.random_interval[0], self.random_interval[1]))

                print("GENERATED: {}".format(self.number_buffer))

                self.number_buffer_full.notify()

    def consume(self):
        while True:
            with self.produce_consume_lock:
                while not self.number_buffer:
                    self.number_buffer_full.wait()

                num1 = self.number_buffer.pop()
                num2 = self.number_buffer.pop()

                print("READ FROM NUMBER BUFFER: {}, {}".format(
                    num2, num1))

                self.number_buffer_empty.notify()

            with self.read_write_result_lock:
                while self.result_buffer:
                    self.result_buffer_empty.wait()

                self.result_buffer.append(is_commensurable(num1, num2))

                self.result_buffer_full.notify()

    def read_write_result(self):
        while True:
            with self.read_write_result_lock:
                while not self.result_buffer:
                    self.result_buffer_full.wait()

                result = self.result_buffer.pop()

                print("READ RESULT: {}".format(result))

                self.result_buffer_empty.notify()

                if result == 1:
                    self.ones_count += 1
                else:
                    self.zeros_count += 1


cc = CommCounter()
threads = []
threads.append(threading.Thread(target=cc.produce))
threads.append(threading.Thread(target=cc.consume))
threads.append(threading.Thread(target=cc.read_write_result))

for t in threads:
    t.start()

for t in threads:
    t.join()
