import threading

mutex = threading.Semaphore(1)

tobacco_sem = threading.Semaphore(1)
paper_sem = threading.Semaphore(1)
match_sem = threading.Semaphore(1)

tobacco_amount = 0
paper_amount = 0
match_amount = 0


# Agent has three different pushers he uses to assign smokers
# Pusher A pushes tobacco onto the Table
def pusher_a():
    global tobacco_amount, paper_amount, match_amount
    mutex.acquire()
    if paper_amount > 0:
        paper_amount -= 1
        match_sem.release()
    elif match_amount > 0:
        match_amount -= 1
        paper_sem.release()
    else:
        tobacco_amount += 1
    mutex.release()


# Pusher B pushes paper onto the Table
def pusher_b():
    global tobacco_amount, paper_amount, match_amount
    mutex.acquire()
    if tobacco_amount > 0:
        tobacco_amount -= 1
        match_sem.release()
    elif match_amount > 0:
        match_amount -= 1
        tobacco_sem.release()
    else:
        paper_amount += 1
    mutex.release()


# Pusher C pushes matches onto the Table
def pusher_c():
    global tobacco_amount, paper_amount, match_amount
    mutex.acquire()
    if tobacco_amount > 0:
        tobacco_amount -= 1
        paper_sem.release()
    elif paper_amount > 0:
        paper_amount -= 1
        tobacco_sem.release()
    else:
        match_amount += 1
    mutex.release()

# Smoker with Tobacco


def smoker_tobacco():
    tobacco_sem.acquire()
    print("smoker with tobacco made a cigarette")
    make_cigarette()
    smoke()


def smoker_paper():
    paper_sem.acquire()
    print("smoker with paper made a cigarette")
    make_cigarette()
    smoke()


def smoker_match():
    match_sem.acquire()
    print("smoker with matches made a cigarette")
    make_cigarette()
    smoke()


def make_cigarette():
    pass


def smoke():
    pass


threads = []

threads.append(threading.Thread(target=pusher_a))
threads.append(threading.Thread(target=pusher_b))
threads.append(threading.Thread(target=pusher_c))

threads.append(threading.Thread(target=smoker_match))
threads.append(threading.Thread(target=smoker_paper))
threads.append(threading.Thread(target=smoker_tobacco))

for t in threads:
    t.start()

