import threading
from random import randint


class ThreadSafeStack:
    def __init__(self):
        self._stack = []
        self._stack_access = threading.Semaphore(1)

    def count(self):
        return len(self._stack)

    def push(self, num):
        self._stack_access.acquire()
        self._stack.append(num)
        self._stack_access.release()

    def pop(self):
        if self.is_empty():
            return None

        self._stack_access.acquire()
        num = self._stack.pop()
        self._stack_access.release()

        return num

    # returns the last element of the stack (top) without removing it
    # not a part of the assignment
    # def top(self):
    #     if self.is_empty():
    #         return None
        
    #     self._stack_access.acquire()
    #     num = self._stack[-1]
    #     self._stack_access.release()

    #     return num

    def is_empty(self):
        self._stack_access.acquire()
        # empty sequences are false
        # (https://www.python.org/dev/peps/pep-0008/#programming-recommendations)
        is_empty = not self._stack
        self._stack_access.release()

        return is_empty