import threading
import time


class Labour:
    def __init__(self, worker_count):
        self._workers = [threading.Thread(
            target=self._work) for id in range(worker_count)]
        self._work_available = threading.Semaphore(0)
        # List of lists in a [future object, function] format, protected by mutex
        self._work_pool = []
        self._work_pool_access = threading.Semaphore(1)
        for worker in self._workers:
            worker.start()

    def _work(self):
        while True:
            self._work_available.acquire()

            self._work_pool_access.acquire()
            # If work is available, get the tuple from _work_pool and
            # do necessary work, then set the future value
            work = self._work_pool.pop()
            future = work[0]
            function = work[1]
            value = function()
            future.set(value)
            self._work_pool_access.release()

    def compute(self, function):
        future = Future()
        work = [future, function]

        self._work_pool_access.acquire()

        self._work_pool.append(work)

        # Notify workers that work is available
        self._work_available.release()
        self._work_pool_access.release()

        return future


class Future:
    def __init__(self):
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._val = None
        self._is_set = False

    def deref(self):
        with self._lock:
            while not self._is_set:
                # Lock caller if the value is not set
                self._condition.wait()
            return self._val

    def set(self, val):
        with self._lock:
            self._val = val
            self._is_set = True
            # Unlock all callers
            self._condition.notify_all()


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def worker_function():
    return factorial(500)


labour = Labour(5)

factorial_future = labour.compute(worker_function)
print(factorial_future.deref())

fibonacci_future = labour.compute(lambda: fibonacci(36))
print(fibonacci_future.deref())

print(fibonacci_future.deref())
