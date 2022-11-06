from collections import defaultdict
from csp import CSP, Constraint
from timer import Timer
from typing import List, Dict, Tuple, Optional
from utils import GridLocation, display_grid


Grid = List[List[int]]
SudokuGrid = List[List[Grid]]
SubGridLocation = Tuple[int, int]


class SudokuGridC(SudokuGrid):
    def __init__(self, grid: Grid) -> None:
        self.grid: Grid = grid
        self.sudoku_grid: SudokuGrid = self._build_sudoku_grid(grid)

    def _build_sudoku_grid(self, grid: Grid) -> SudokuGrid:
        sudoku_grid: SudokuGrid = [
            [generate_empty_grid(3) for _ in range(3)]
            for _ in range(3)
        ]
        for row, nums in enumerate(grid):
            for col, n in enumerate(nums):
                sudoku_grid[row // 3][col // 3][row % 3][col % 3] = n
        return sudoku_grid

    def _get_missing_numbers_by_grid(self) -> Dict[SubGridLocation, List[int]]:
        numbers_by_grid: Dict[SubGridLocation, List[int]] = defaultdict(list)
        for g_row, grids in enumerate(self.sudoku_grid):
            for g_col, grid in enumerate(grids):
                for nums in grid:
                    for n in nums:
                        if n > 0:
                            numbers_by_grid[(g_row, g_col)].append(n)

        missing_nums_by_grid: Dict[SubGridLocation, List[int]] = defaultdict(list)
        for grid, numbers in numbers_by_grid.items():
            missing_nums_by_grid[grid] = [n for n in range(1, 10) if n not in numbers]
        return missing_nums_by_grid

    def _get_numbers_by_row_and_col(self) -> Dict[int, List[int]]:
        numbers_by_row: Dict[int, List[int]] = defaultdict(list)
        numbers_by_col: Dict[int, List[int]] = defaultdict(list)
        for row, nums in enumerate(self.grid):
            for col, n in enumerate(nums):
                if n > 0:
                    numbers_by_row[row].append(n)
                    numbers_by_col[col].append(n)
        return numbers_by_row, numbers_by_col

    def get_domains(self) -> Dict[GridLocation, List[int]]:
        numbers: List[int] = list(range(1, 10))
        possible_nums_by_grid_loc: Dict[GridLocation, List[int]] = defaultdict(list)
        for g_row, grids in enumerate(self.sudoku_grid):
            for g_col, grid in enumerate(grids):
                for row, nums in enumerate(grid):
                    for col, n in enumerate(nums):
                        gl = GridLocation((g_row * 3) + row, (g_col * 3) + col)
                        if n == 0:
                            possible_nums_by_grid_loc[gl] = numbers
                        else:
                            possible_nums_by_grid_loc[gl] = [n]
        return possible_nums_by_grid_loc

    def get_domains_opt1(self) -> Dict[GridLocation, List[int]]:
        all_nums = list(range(1, 10))
        missing_nums_by_grid: Dict[SubGridLocation, List[int]] = self._get_missing_numbers_by_grid()

        possible_nums_by_grid_loc: Dict[GridLocation, List[int]] = defaultdict(list)
        for g_row, grids in enumerate(self.sudoku_grid):
            for g_col, grid in enumerate(grids):
                for row, nums in enumerate(grid):
                    for col, n in enumerate(nums):
                        gl = GridLocation((g_row * 3) + row, (g_col * 3) + col)
                        if n == 0:
                            missing_nums = missing_nums_by_grid.get((g_row, g_col)) or all_nums
                            possible_nums_by_grid_loc[gl] = missing_nums
                        else:
                            possible_nums_by_grid_loc[gl] = [n]
        return possible_nums_by_grid_loc

    def get_domains_opt2(self) -> Dict[GridLocation, List[int]]:
        all_nums = list(range(1, 10))
        missing_nums_by_grid: Dict[SubGridLocation, List[int]] = self._get_missing_numbers_by_grid()
        nums_by_row, nums_by_col  = self._get_numbers_by_row_and_col()

        possible_nums_by_grid_loc: Dict[GridLocation, List[int]] = defaultdict(list)
        for g_row, grids in enumerate(self.sudoku_grid):
            for g_col, grid in enumerate(grids):
                for row, nums in enumerate(grid):
                    for col, n in enumerate(nums):
                        gl = GridLocation((g_row * 3) + row, (g_col * 3) + col)
                        if n == 0:
                            missing_nums = missing_nums_by_grid.get((g_row, g_col)) or all_nums
                            possible_nums_by_grid_loc[gl] = [
                                n
                                for n in missing_nums
                                if n not in nums_by_row[gl.row]
                                and n not in nums_by_col[gl.col]
                            ]
                        else:
                            possible_nums_by_grid_loc[gl] = [n]

        return possible_nums_by_grid_loc

    def __str__(self) -> str:
        length: int = 25
        output: str = length * '—' + '\n'
        for row, nums in enumerate(self.grid):
            for col, n in enumerate(nums):
                if col == 0:
                    output += '| '
                output += str(n) + ' ' if n > 0 else '  '
                if col % 3 == 2:
                    output += '| '
            output += '\n'
            if row % 3 == 2:
                output += length * '—' + '\n'
        return output


class SudokuConstraint(Constraint[GridLocation, int]):
    def __init__(self, locations: List[GridLocation]) -> None:
        super().__init__(locations)
        self.locations: List[GridLocation] = locations

    def is_satisfied(self, assignment: Dict[GridLocation, int]) -> bool:

        def check_numbers(numbers: List[int]):
            return sorted(list(set(numbers))) == sorted(numbers)

        numbers_by_row: Dict[int, List[int]] = defaultdict(list)
        numbers_by_col: Dict[int, List[int]] = defaultdict(list)
        numbers_by_sub_grid: Dict[SubGridLocation, List[int]] = defaultdict(list)
        for loc, n in assignment.items():
            numbers_by_row[loc.row].append(n)
            numbers_by_col[loc.col].append(n)
            numbers_by_sub_grid[(loc.row // 3, loc.col // 3)].append(n)
        return all([
            check_numbers(numbers)
            for element in [numbers_by_row, numbers_by_col, numbers_by_sub_grid]
            for numbers in element.values()
        ])


def generate_empty_grid(n) -> Grid:
    return [
        [0 for _ in range(n)]
        for _ in range(n)
    ]


def insert_solution_into_grid(solution: Dict[GridLocation, int]) -> Grid:
    grid = generate_empty_grid(9)
    for loc, n in solution.items():
        grid[loc.row][loc.col] = n
    return grid


if __name__ == '__main__':
    timer = Timer(timer_type="performance")
    timer.start()

    grid: Grid = [
        [0, 7, 0, 0, 1, 4, 0, 0, 0],
        [6, 1, 2, 0, 9, 5, 3, 8, 0],
        [3, 0, 4, 0, 6, 8, 9, 7, 1],
        [0, 0, 0, 1, 0, 0, 0, 5, 0],
        [2, 8, 0, 0, 0, 0, 7, 0, 3],
        [5, 0, 3, 0, 8, 0, 0, 0, 0],
        [0, 2, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 6, 8, 0, 0, 1, 0, 5],
        [0, 0, 0, 6, 7, 0, 4, 3, 0],
    ]
    # grid = generate_empty_grid(9)

    sudoku_grid: SudokuGrid = SudokuGridC(grid)
    print(sudoku_grid)

    domains: Dict[GridLocation, List[int]] = sudoku_grid.get_domains_opt2()
    locations: List[GridLocation] = domains.keys()

    csp: CSP[GridLocation, List[int]] = CSP(locations, domains)
    csp.add_constraint(SudokuConstraint(locations))

    solution: Optional[Dict[GridLocation, int]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        solved_sudoku_grid: SudokuGrid = SudokuGridC(insert_solution_into_grid(solution))
        print(solved_sudoku_grid)

    timer.stop()
    print(f'-> elapsed time: {timer.time_sec}')
