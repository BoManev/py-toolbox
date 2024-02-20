def simple_memo(f):
    cache = {}

    def wrapper(*args):
        args = tuple(args)
        if args not in cache:
            print("[cache] miss")
            cache[args] = f(*args)
        else:
            print("[cache] hit")
        return cache[args]

    return wrapper


@simple_memo
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


fib(10)
