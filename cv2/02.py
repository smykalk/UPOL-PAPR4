import threading
import time
from random import randint

def sleep_then_print(thread_num):
    sleep_time = randint(0,10)
    time.sleep(sleep_time)
    print("Thread {} slept for {} seconds".format(thread_num, sleep_time))

thread = []

thread.append(threading.Thread(target=sleep_then_print,args=(1,)))
thread.append(threading.Thread(target=sleep_then_print,args=(2,)))

thread[0].start()
thread[1].start()

thread[0].join()
thread[1].join()