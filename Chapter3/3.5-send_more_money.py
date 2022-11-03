from csp import Constraint, CSP
from typing import Dict, List, Optional


class SendMoreMoneyConstraint(Constraint[str, int]):
    def __init__(self, letters: List[str]) -> None:
        super().__init__(letters)
        self.letters: List[str] = letters

    def is_satisfied(self, assignment: Dict[str, int]) -> bool:
        # if there are duplicate values, then it's not a solution
        if len(set(assignment.values())) < len(assignment):
            return False

        # if all variables have been assigned, check if it adds correctly
        if len(assignment) == len(self.letters):
            send: int = \
                assignment['S'] * 1000 + \
                assignment['E'] * 100 + \
                assignment['N'] * 10 + \
                assignment['D']
            more: int = \
                assignment['M'] * 1000 + \
                assignment['O'] * 100 + \
                assignment['R'] * 10 + \
                assignment['E']
            money: int = \
                assignment['M'] * 10000 + \
                assignment['O'] * 1000 + \
                assignment['N'] * 100 + \
                assignment['E'] * 10 + \
                assignment['Y']
            return send + more == money

        return True  # no conflict


def display_solution(solution: Dict[str, int]) -> None:
    phrase: str = 'SEND + MORE = MONEY'
    print(phrase)

    new_phrase = ''
    for letter in phrase:
        if letter in solution:
            new_phrase += str(solution[letter])
        else:
            new_phrase += letter
    print(new_phrase)


if __name__ == '__main__':
    letters: List[str] = list(set([char for char in 'SENDMOREMONEY']))

    possible_digits: Dict[str, List[int]] = {}
    for letter in letters:
        possible_digits[letter] = range(10)

    possible_digits['M'] = [1]  # so we don't get answers starting with a 0

    csp: CSP[str, int] = CSP(letters, possible_digits)

    csp.add_constraint(SendMoreMoneyConstraint(letters))

    solution: Optional[Dict[str, int]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print(solution)
        display_solution(solution)

