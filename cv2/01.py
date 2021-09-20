import threading

number = 0

def increment_ntimes(n):
    global number
    while n > 0:
        number += 1
        n -= 1

thread = []

thread.append(threading.Thread(target=increment_ntimes, args=(1000000,)))
thread.append(threading.Thread(target=increment_ntimes, args=(1000000,)))

thread[0].start()
thread[1].start()

thread[0].join()
thread[1].join()

print(number)