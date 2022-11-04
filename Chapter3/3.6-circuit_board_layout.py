from csp import Constraint, CSP
from itertools import cycle
from termcolor import colored
from typing import Dict, List, Optional, Tuple
from utils import Grid, GridLocation, display_grid


Rectangle = Tuple[int, int]  # type alias for rectangles


class CircuitBoardConstraint(Constraint[Rectangle, List[GridLocation]]):
    def __init__(self, rectangles: List[Rectangle]) -> None:
        super().__init__(rectangles)
        self.rectangles: List[Rectangle] = rectangles

    def is_satisfied(self, assignment: Dict[Rectangle, List[GridLocation]]) -> bool:
        # if there are any duplicates grid locations, then there is an overlap
        all_locations = [
            locs
            for values in assignment.values()
            for locs in values
        ]
        return len(set(all_locations)) == len(all_locations)


def generate_grid(rows: int, cols: int, ) -> Grid:
    # initialize grid with empty spaces
    return [
        ['□' for _ in range(cols)]
        for _ in range(rows)
    ]


def generate_domain(rectangle: Rectangle, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    side1: int = rectangle[0]
    side2: int = rectangle[1]

    def get_grid_locations(row: int, col: int, s1: int, s2: int):
        return [
            GridLocation(r, c)
            for r in range(row, row + s1)
            for c in range(col, col + s2)
        ]

    for row in range(height):
        for col in range(width):
            # in one direction
            if row + side1 <= height and col + side2 <= width:
                domain.append(get_grid_locations(row, col, side1, side2))
            # if not square, in other direction
            if side1 != side2 and row + side2 <= height and col + side1 <= width:
                domain.append(get_grid_locations(row, col, side2, side1))
    return domain


def insert_solution_into_grid(
    solution: Optional[Dict[Rectangle, List[GridLocation]]],
    grid: Grid
) -> None:
    colors = cycle(['blue', 'yellow', 'green', 'magenta', 'cyan', 'red'])
    for rectangle, grid_locations in solution.items():
        color = next(colors)
        for loc in grid_locations:
            grid[loc.row][loc.col] = colored('■', color)


if __name__ == '__main__':
    grid: Grid = generate_grid(9, 9)

    rectangles: List[Rectangle] = [
        (1, 6),
        (2, 2),
        (2, 5),
        (3, 3),
        (4, 4),
    ]

    locations: Dict[Rectangle, List[List[GridLocation]]] = {}
    for rectangle in rectangles:
        locations[rectangle] = generate_domain(rectangle, grid)

    csp: CSP[Rectangle, List[GridLocation]] = CSP(rectangles, locations)
    csp.add_constraint(CircuitBoardConstraint(rectangles))

    solution: Optional[Dict[Rectangle, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        insert_solution_into_grid(solution, grid)
        display_grid(grid)
