from functools import lru_cache


@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    if n < 2:  # base case
        return n

    return fib4(n - 2) + fib4(n - 1)  # recursive case


if __name__ == "__main__":
    for i in range(10):
        print("{} -> {}".format(i, fib4(i)))
