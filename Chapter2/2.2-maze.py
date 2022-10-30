from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from generic_search import dfs, bfs, a_star, node_to_path, Node


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    col: int


class Maze:
    def __init__(
        self,
        rows: int = 10,
        cols: int = 10,
        sparseness: float = 0.2,
        start: MazeLocation = MazeLocation(0,0),
        goal: MazeLocation = MazeLocation(9,9),
    ) -> None:
        # initialize basic instance variables
        self.rows: int = rows
        self.cols: int = cols
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # fill the grid with empty cells and randomly populate it with blocked cells
        self.grid: List[List[Cell]] = self._get_randomly_filled_grid(sparseness)

    def _get_randomly_filled_grid(self, sparseness: float) -> List[List[Cell]]:
        grid: List[List[Cell]] = [[Cell.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if random.uniform(0, 1.0) < sparseness:
                    grid[row][col] = Cell.BLOCKED
        return grid

    def __str__(self) -> str:
        output: str = ""
        for row in self.grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row + 1 < self.rows and self.grid[ml.row + 1][ml.col] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.col))
        if ml.row - 1 >= 0 and self.grid[ml.row - 1][ml.col] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.col))
        if ml.col + 1 < self.cols and self.grid[ml.row][ml.col + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.col + 1))
        if ml.col - 1 >= 0 and self.grid[ml.row][ml.col - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.col - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self.grid[maze_location.row][maze_location.col] = Cell.PATH
        self.grid[self.start.row][self.start.col] = Cell.START
        self.grid[self.goal.row][self.goal.col] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self.grid[maze_location.row][maze_location.col] = Cell.EMPTY
        self.grid[self.start.row][self.start.col] = Cell.START
        self.grid[self.goal.row][self.goal.col] = Cell.GOAL


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        x_dist: int = ml.col - goal.col
        y_dist: int = ml.row - goal.row
        return sqrt((x_dist ** 2) + (y_dist ** 2))
    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        x_dist: int = abs(ml.col - goal.col)
        y_dist: int = abs(ml.row - goal.row)
        return (x_dist + y_dist)
    return distance


if __name__ == "__main__":
    search_algo_by_name = {
        'depth-first search': dfs,
        'breadth-first search': bfs,
        'A*': a_star,
    }

    maze: Maze = Maze()
    print(maze)

    for name, search_algo in search_algo_by_name.items():
        params = {
            'initial': maze.start,
            'goal_test': maze.goal_test,
            'successors': maze.successors,
        }
        if name == 'A*':
            params['heuristic'] = manhattan_distance(maze.goal)
        solution: Optional[Node[MazeLocation]] = search_algo(**params)

        if solution is None:
            print("No solution found using {}!".format(name))
        else:
            print("=== Solution by {} ===".format(name))
            path: List[MazeLocation] = node_to_path(solution)
            print("-> path's length: {}".format(len(path)))
            maze.mark(path)
            print("-> solved maze:")
            print(maze)
            maze.clear(path)
