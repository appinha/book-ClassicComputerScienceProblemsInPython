from csp import CSP, Constraint
from itertools import cycle
from random import choice
from string import ascii_uppercase
from termcolor import colored
from typing import List, Dict, Optional
from utils import Grid, GridLocation, display_grid


class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def is_satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # if there are any duplicates grid locations, then there is an overlap
        all_locations = [
            locs
            for values in assignment.values()
            for locs in values
        ]
        return len(set(all_locations)) == len(all_locations)


def generate_grid(rows: int, cols: int) -> Grid:
    # initialize grid with random letters
    return [
        [choice(ascii_uppercase) for _ in range(cols)]
        for _ in range(rows)
    ]


def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)

    for row in range(height):
        for col in range(width):
            cols: range = range(col, col + length)
            rows: range = range(row, row + length)
            if col + length <= width:
                # left to right
                domain.append([GridLocation(row, c) for c in cols])
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])
            if row + length <= height:
                # top to bottom
                domain.append([GridLocation(r, col) for r in rows])
                # diagonal towards bottom left
                if col - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])
    return domain


def insert_solution_into_grid(
    solution: Optional[Dict[str, List[GridLocation]]],
    grid: Grid
) -> None:
    colors = cycle(['blue', 'yellow', 'green', 'magenta', 'cyan', 'red'])
    for word, grid_locations in solution.items():
        color = next(colors)
        # random reverse half the time
        if choice([True, False]):
            grid_locations.reverse()
        for i, letter in enumerate(word):
            (row, col) = (grid_locations[i].row, grid_locations[i].col)
            grid[row][col] = colored(letter, color)


if __name__ == '__main__':
    grid: Grid = generate_grid(9, 9)

    words: List[str] = [
        'MATTHEW',
        'JOE',
        'MARY',
        'SARAH',
        'SALLY',
    ]

    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)

    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))

    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        insert_solution_into_grid(solution, grid)
        display_grid(grid)
