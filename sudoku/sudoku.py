#!/usr/bin/env python
import re
from pprint import pprint
import pycosat

class Variable(object):
    """Named variable to be passed to a SAT solver.

    This class represents variables as strings and has convenience
    functions for negation, and, and or.
    """
    def __init__(self, name, polarity=True):
        self.name = name
        self.polarity = polarity

    def __neg__(self):
        return Variable(self.name, not self.polarity)

    def __inv__(self):
        return self.__neg__()

    def __str__(self):
        return '%s%s' % ('' if self.polarity else '-', self.name)

    def __repr__(self):
        return self.__str__()


def clauses_to_ints(vclauses):
    name_to_int = {}
    iclauses = []
    for clause in vclauses:
        iclause = []
        for var in clause:
            i = name_to_int.setdefault(var.name, len(name_to_int) + 1)
            iclause.append(i if var.polarity else -i)
        iclauses.append(iclause)

    return name_to_int, iclauses


def solve(grid):
    clauses = sudoku_clauses()

    # add nonzeros
    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val:
                clauses.append([v(i+1, j+1, val)])

    name_to_int, iclauses = clauses_to_ints(clauses)

    result = pycosat.solve(iclauses)

    for i in range(9):
        for j in range(9):
            for d in range(1, 10):
                var = v(i+1, j+1, d)
                x = name_to_int[var.name]
                if result[x-1] > 0:
                    grid[i][j] = d


def v(i, j, d):
    """name for variable representing cell[i,j] == d"""
    return Variable("%d%d_eq_%d" % (i, j, d))


def sudoku_clauses():
    clauses = []

    for i in range(1, 10):
        for j in range(1, 10):
            # all cells are set to at least one of 1-9
            clauses.append([v(i, j, d) for d in range(1, 10)])

            # no cell has more than one value set.
            for d in range(1, 10):
                for e in range(d + 1, 10):
                    clauses.append([-v(i, j, d), -v(i, j, e)])

    def valid(cells):
        """Clauses requiring a set of cells to have distinct values.

        cells is a list of tuples (i, j)
        """
        for i, c1 in enumerate(cells):
            for j, c2 in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        clauses.append(
                            [-v(c1[0], c1[1], d), -v(c2[0], c2[1], d)])

    # ensure each row, column, and ninth is valid (contains all numbers)

    # rows
    for i in range(1, 10):
        row = zip([i] * 9, range(1, 10))
        valid(row)

    # cols
    for j in range(1, 10):
        col = zip(range(1, 10), [j] * 9)
        valid(col)

    # ninths
    for k in range(3):
        for l in range(3):
            ninth = [(i, j)
                     for i in range(k * 3 + 1, k * 3 + 4)
                     for j in range(l * 3 + 1, l * 3 + 4)]
            valid(ninth)

    return clauses


if __name__ == '__main__':
    # hard Sudoku problem, see Fig. 3 in paper by Weber
    hard = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]

    hard = [[0, 5, 3, 0, 1, 0, 8, 6, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 3, 0, 0, 0, 5],
            [0, 8, 7, 0, 0, 0, 9, 4, 0],
            [0, 0, 0, 9, 0, 3, 0, 0, 0],
            [0, 9, 5, 0, 0, 0, 3, 2, 0],
            [0, 7, 0, 1, 0, 2, 0, 3, 0],
            [0, 6, 1, 0, 0, 0, 7, 8, 0],
            [2, 0, 0, 0, 7, 0, 0, 0, 9]]

    solve(hard)

    pprint(hard)
    exit()
    assert [[1, 2, 6, 4, 3, 7, 9, 5, 8],
            [8, 9, 5, 6, 2, 1, 4, 7, 3],
            [3, 7, 4, 9, 8, 5, 1, 2, 6],
            [4, 5, 7, 1, 9, 3, 8, 6, 2],
            [9, 8, 3, 2, 4, 6, 5, 1, 7],
            [6, 1, 2, 5, 7, 8, 3, 9, 4],
            [2, 6, 9, 3, 1, 4, 7, 8, 5],
            [5, 4, 8, 7, 6, 9, 2, 3, 1],
            [7, 3, 1, 8, 5, 2, 6, 4, 9]] == hard
