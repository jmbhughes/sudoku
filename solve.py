import sys

# the coordinate system
rows = 'ABCDEFGHI'  # the rows are named by letters
cols = '123456789'  # the columns are named by numbers

# lets first create a set of all the squares
squares = [r+c for r in rows for c in cols]
assert(len(squares) == 81)  # there are 81 squares

# now we will collect all the units together for checking validity
all_units = ([[r+c for c in cols] for r in rows] +  # the set of columns
             [[r+c for r in rows] for c in cols] +  # the set of rows
             [[r+c for r in rs for c in cs] for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])  # blocks
assert(len(all_units) == 27)  # there are 27 units

# we can now map each square to its units
units = {s: [u for u in all_units if s in u] for s in squares}
assert(all(len(units[s]) == 3 for s in squares))  # each square should belong to three units, its row, column, and block

# peers are the set of squares that share units
peers = {s: (set([sq for u in units[s] for sq in u]) - {s}) for s in squares}
assert(all(len(peers[s]) == 20 for s in squares))


def assign(solution, square, value):
    """
    Assign a value to a given square.
    :param solution: current solution for grid
    :param square: square to assign
    :param value: value to assign
    """

    # We must eliminate this value from the other squares that this square's peer because they're no longer an option
    for other in solution[square].replace(value, ''):
        eliminate(solution, square, other)


def eliminate(solution, square, value):
    """
    Conduct constraint propagation
    Eliminate the value from all the peer squares as a possibility and then conclude what is possible then
    :param solution: current solution for sudoku grid
    :param square: coordinates for square in question
    :param value: value to eliminate for the square
    """
    if value not in solution[square]:
        return

    # remove the value from the current square
    solution[square] = solution[square].replace(value, '')

    # if the resulting length of our square's solution, we know we have found the answer! so we can then eliminate
    # our final answer from any of the square's peers.
    if len(solution[square]) == 1:
        last = solution[square][0]
        for p in peers[square]:
            eliminate(solution, p, last)

    # now we do the second check and iterate over the units. If we find any number can only go in one square in the unit
    # then we know that square has to use that number so we assign it automatically
    for u in units[square]:
        candidates = [s for s in u if value in solution[s]]
        if len(candidates) == 1:
            assign(solution, candidates[0], value)


def is_filled(solution):
    """
    Determines if all the squares only have one option remaining
    :param solution: current solution for the grid
    :return: True if all squares are filled, False otherwise meaning more searching needed
    """
    return all(len(solution[s]) == 1 for s in squares)


def search(solution):
    """
    Perform a search for solutions if constraint propagation failed.
    :param solution: current solution for the grid
    :return: True if a solution is reached, False if not
    """
    # If any of the squares have no options then there is no solution
    if any(not solution[s] for s in squares):
        return False
    # if all the the squares have only one option remaining we already have a solution
    elif is_filled(solution):
        return True
    # actually attempt the search
    else:
        # find the square that has the minimum number of options remaining, we are most certain about its solution
        square = min((s for s in squares if len(solution[s]) > 1), key=lambda s: len(solution[s]))

        # make a copy if we need to backtrack
        orig = solution.copy()

        # search by trying each possibility for that square
        for value in orig[square]:

            # attempt to assign it
            assign(solution, square, value)

            # continue searching, if we're successful return true
            if search(solution):
                return True
            else:  # if we're unsuccessful backtrack and try the next option
                solution.update(orig)
        else:  # we get out of the loop without finding a solution so this puzzle is unsolvable!
            return False


def print_grid(grid):
    """
    Print the grid prettily
    :param grid: the sudoku
    :return:
    """
    max_len = max(len(grid[s]) for s in squares if grid[s])
    for r in rows:
        for c in cols:
            print('{val:^{width}} '.format(val=grid[r+c] if grid[r+c] else '-', width=max_len), end='')
        print()


# an example puzzle
puzzle = '''4.....8.5
            .3.......
            ...7.....
            .2.....6.
            ....8.4..
            ....1....
            ...6.3.7.
            5..2.....
            1.4......'''


def parse_puzzle(position):
    """
    Construct our data type from a string
    :param position:
    :return:
    """
    puzzle = [c if c in '123456789' else None for c in position if c not in ' \n']
    assert(len(puzzle) == 81)  # the deconstructed puzzle must have 81 squares!
    return {squares[i]: puzzle[i] for i in range(0, len(squares))}


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    # initially every square has every option in the solution
    solution = {s: '123456789' for s in squares}
    puz_str = ''.join(lines)

    # parse the puzzles from the string
    puz = parse_puzzle(puz_str)
    print('Puzzle:\n')
    print_grid(puz)

    # attempt to solve the puzzle by assigning the known values
    for sq, val in puz.items():
        if val:
            assign(solution, sq, val)

    if all(len(solution[s]) == 1 for s in squares):
        print('\nSolved by pure constraint propagation:\n')
    else:  # constraint propagation was insufficient
        print('\nConstraint propagation result:\n')
        print_grid(solution)

        # attempt a search!
        search(solution)
        print('\nSearch result:\n')

    print_grid(solution)
