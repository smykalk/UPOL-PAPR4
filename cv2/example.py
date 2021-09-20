import threading
from random import randint 

# Thread constructor takes a function as its argument
def thread_print():
    print("Hello world")

thread = threading.Thread(target=thread_print)

# start the thread
thread.start()

# join the thread to current thread
# the thread in which the 'thread' thread has been started
# waits for 'thread' to finish
thread.join()


# Passing arguments to threads

def thread_argument(text):
    print(text)

thread = threading.Thread(target=thread_argument, args=("Hello World!,"))
thread.start
thread.join

number = 10

def add_value(n):
    global number
    number += n


thread = threading.Thread(target=add_value, args=(20,))
thread.start()
thread.join()

print(number)