from concurrent.futures import ThreadPoolExecutor, as_completed


def fib(n):
    a, b = 0, 1
    for i in range(0, n):
        a, b = b, a + b
    return ((n, a))


def parallel_fib(x, thread_count):
    numbers = list(range(x + 1))
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        fibonacci_results = {executor.submit(fib, n,): n for n in numbers}

        for future in as_completed(fibonacci_results):
            n, f = future.result()
            print("{0}: {1}".format(n, f))


parallel_fib(30,10)
