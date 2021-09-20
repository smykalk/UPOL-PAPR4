import concurrent.futures


def _fib(n):
    if n < 2:
        return n

    x = _fib(n - 1)
    y = _fib(n - 2)

    return x + y


def _fibp(pos, executor):
    if pos < 2:
        return pos

    x = executor.submit(_fib, (pos - 1))
    y = executor.submit(_fib, (pos - 2))

    return x.result() + y.result()


def para_fib(n, workers=1):
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        position = 30
        return _fibp(position, executor)


print(para_fib(35, 10))
