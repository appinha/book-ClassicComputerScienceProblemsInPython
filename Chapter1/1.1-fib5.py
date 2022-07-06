def fib5(n: int) -> int:
    if n == 0:  # special case
        return n

    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
    return next


if __name__ == "__main__":
    for i in range(10):
        print("{} ->".format(i), fib5(i))