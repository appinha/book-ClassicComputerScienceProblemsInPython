from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


C = TypeVar('C', bound='Comparable')
T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(
        self,
        state: T,
        parent: Optional[Node],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


def linear_search(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


def binary_search(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]

    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)

    path.reverse()
    return path


def dfs(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
) -> Optional[Node[T]]:
    # frontier is where we have yet to go
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))

    # explored is where we have been
    explored: Set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node

        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def bfs(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
) -> Optional[Node[T]]:
    # frontier is where we have yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))

    # explored is where we have been
    explored: Set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node

        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def a_star(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], float],
) -> Optional[Node[T]]:
    # frontier is where we have yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))

    # explored is where we have been
    explored: Dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node

        # check where we can go next and haven't explored
        for child in successors(current_state):
            # 1 assumes a grid, need a cost function for more sophisticated apps
            new_cost: float = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))

    return None  # went through everything and never found goal


if __name__ == '__main__':
    print(linear_search([1, 5, 15, 15, 15, 15, 20], 5))  # True
    print(binary_search(['a', 'd', 'e', 'f', 'z'], 'f'))  # True
    print(binary_search(['john', 'mark', 'ronald', 'sarah'], 'sheila'))  # False
