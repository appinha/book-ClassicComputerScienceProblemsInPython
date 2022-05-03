from typing import Dict


memo: Dict[int, int] = {0: 0, 1: 1}  # base cases


def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)  # memoization

    return memo[n]


if __name__ == "__main__":
    for i in range(10):
        print("{} ->".format(i), fib3(i))
