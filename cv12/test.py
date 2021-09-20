from concurrent.futures import ThreadPoolExecutor
import threading
from random import randint

def task(id):
    print("Executing {} Task".format(id))
    result = pow(randint(1, 10), randint(2, 9))
    print("{} Task finished.".format(id))
    return result


    # Automaticky po dokonceni vypoctu
with ThreadPoolExecutor(max_workers=2) as executor:
    future1 = executor.submit(task, 1)
    future2 = executor.submit(task, 2)

    print("Result 1 = {}".format(future1.result()))
    print("Result 2 = {}".format(future2.result()))