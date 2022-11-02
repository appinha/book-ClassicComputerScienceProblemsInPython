from csp import Constraint, CSP
from pprint import pprint
from typing import Dict, List, Optional


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def is_satisfied(self, assignment: Dict[str, str]) -> bool:
        # if either place is not in the assignment, then it's not yet possible for their colors to
        # be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the color assigned to place2
        return assignment[self.place1] != assignment[self.place2]


if __name__ == '__main__':
    variables: List[str] = [
        'Western Australia',
        'Northern Territory',
        'South Australia',
        'Queensland',
        'New South Wales',
        'Victoria',
        'Tasmania',
    ]

    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ['red', 'green', 'blue']

    csp: CSP[str, str] = CSP(variables, domains)

    borders: List[List[str]] = [
        ['Western Australia', 'Northern Territory'],
        ['Western Australia', 'South Australia'],
        ['South Australia', 'Northern Territory'],
        ['South Australia', 'Queensland'],
        ['South Australia', 'New South Wales'],
        ['South Australia', 'Victoria'],
        ['Queensland', 'Northern Territory'],
        ['Queensland', 'New South Wales'],
        ['Victoria', 'New South Wales'],
        ['Victoria', 'Tasmania'],
    ]
    for border in borders:
        csp.add_constraint(MapColoringConstraint(*border))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        pprint(solution)
