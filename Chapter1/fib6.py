from typing import Generator


def fib6(n: int) -> Generator[int, None, None]:
    yield 0  # special case

    if n > 0:  # special case
        yield 1

    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
        yield next  # main generation step


if __name__ == "__main__":
    for i in range(10):
        print("{} -> {}".format(i, list(fib6(i))))