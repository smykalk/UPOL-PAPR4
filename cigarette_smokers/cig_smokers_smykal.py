import threading

agent_sem = threading.Semaphore(1)
tobacco = threading.Semaphore(0)
paper = threading.Semaphore(0)
match = threading.Semaphore(0)
is_tobacco = is_paper = is_match = False
tobacco_sem = threading.Semaphore(0)
paper_sem = threading.Semaphore(0)
match_sem = threading.Semaphore(0)

mutex = threading.Semaphore(1)


def agent_a():
    while True:
        agent_sem.acquire()
        tobacco.release()
        paper.release()


def agent_b():
    while True:
        agent_sem.acquire()
        paper.release()
        match.release()


def agent_c():
    while True:
        agent_sem.acquire()
        tobacco.release()
        match.release()


def pusher_a():
    global is_tobacco, is_match, is_paper
    while True:
        tobacco.acquire()
        mutex.acquire()

        if is_paper:
            is_paper = False
            match_sem.release()
        elif is_match:
            is_match = False
            paper_sem.release()
        else:
            is_tobacco = True

        mutex.release()


def pusher_b():
    global is_tobacco, is_match, is_paper
    while True:
        match.acquire()
        mutex.acquire()

        if is_tobacco:
            is_tobacco = False
            paper_sem.release()
        elif is_paper:
            is_paper = False
            tobacco_sem.release()
        else:
            is_match = True

        mutex.release()


def pusher_c():
    global is_tobacco, is_match, is_paper
    while True:
        paper.acquire()
        mutex.acquire()

        if is_tobacco:
            is_tobacco = False
            match_sem.release()
        elif is_match:
            is_match = False
            tobacco_sem.release()
        else:
            is_paper = True

        mutex.release()


def smoker_tobacco():
    while True:
        tobacco_sem.acquire()
        make_cigarette()
        print("Smoker with tobacco made a cigarette")
        agent_sem.release()
        smoke()


def smoker_match():
    while True:
        match_sem.acquire()
        make_cigarette()
        print("Smoker with matches made a cigarette")
        agent_sem.release()
        smoke()


def smoker_paper():
    while True:
        paper_sem.acquire()
        make_cigarette()
        print("Smoker with papers made a cigarette")
        agent_sem.release()
        smoke()


def make_cigarette():
    pass


def smoke():
    pass


threads = []
threads.append(threading.Thread(target=agent_a))
threads.append(threading.Thread(target=agent_b))
threads.append(threading.Thread(target=agent_c))
threads.append(threading.Thread(target=pusher_a))
threads.append(threading.Thread(target=pusher_b))
threads.append(threading.Thread(target=pusher_c))
threads.append(threading.Thread(target=smoker_match))
threads.append(threading.Thread(target=smoker_paper))
threads.append(threading.Thread(target=smoker_tobacco))


for t in threads:
    t.start()
