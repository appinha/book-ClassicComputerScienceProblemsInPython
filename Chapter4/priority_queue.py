from typing import Generic, List, TypeVar
from heapq import heappush, heappop


T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)
