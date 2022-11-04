from csp import Constraint, CSP
from termcolor import colored
from typing import Dict, List, Optional, Tuple


class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns: List[int]) -> None:
        super().__init__(columns)
        self.columns: List[int] = columns

    def is_satisfied(self, assignment: Dict[int, int]) -> bool:
        # q1c = queen 1's column, q1r = queen 1's row
        for q1c, q1r in assignment.items():
            for q2c in range(q1c + 1, len(self.columns) + 1):
                if q2c in assignment:
                    q2r: int = assignment[q2c]
                    if q1r == q2r:  # queens are on same row
                        return False
                    if abs(q1r - q2r) == abs(q1c - q2c):  # queens are on same diagonal
                        return False
        return True  # no conflicts


def display_queens_on_board(solution: Dict[int, int]) -> None:
    for col in range(1, 9):
        line = ''
        for row in range(1, 9):
            if solution[col] == row:
                line += colored('★  ', 'yellow')
            else:
                line += '□  '
        print(line)


if __name__ == '__main__':
    columns: List[int] = range(1, 9)

    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = range(1, 9)

    csp: CSP[int, int] = CSP(columns, rows)

    csp.add_constraint(QueensConstraint(columns))

    solution: Optional[Dict[int, int]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        display_queens_on_board(solution)
