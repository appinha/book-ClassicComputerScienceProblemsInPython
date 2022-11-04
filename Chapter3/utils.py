from typing import List, NamedTuple


Grid = List[List[str]]  # type alias for grids


class GridLocation(NamedTuple):
    row: int
    col: int


def display_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(row))
