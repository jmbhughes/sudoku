rows = 'ABCDEFGHI'
cols = '123456789'

squares = [r+c for r in rows for c in cols]
assert(len(squares) == 81)

all_units = ([[r+c for c in cols] for r in rows] +
             [[r+c for r in rows] for c in cols] +
             [[r+c for r in rs for c in cs]
              for rs in ('ABC', 'DEF', 'GHI')
              for cs in ('123', '456', '789')])
assert(len(all_units) == 27)

units = {s: [u for u in all_units if s in u] for s in squares}
assert(all(len(units[s]) == 3 for s in squares))

peers = {s: (set([sq for u in units[s] for sq in u]) - {s})
         for s in squares }
assert(all(len(peers[s]) == 20 for s in squares))


def assign(sol, sq, val):
    for other in sol[sq].replace(val, ''):
        eliminate(sol, sq, other)


def eliminate(sol, sq, val):
    if val not in sol[sq]:
        return
    sol[sq] = sol[sq].replace(val, '')
    if len(sol[sq]) == 1:
        last = sol[sq][0]
        for p in peers[sq]:
            eliminate(sol, p, last)
    for u in units[sq]:
        candidates = [s for s in u if val in sol[s]]
        if len(candidates) == 1:
            assign(sol, candidates[0], val)


def search(sol):
    if any(not sol[s] for s in squares):
        return False
    elif all(len(sol[s]) == 1 for s in squares):
        return True
    else:
        sq = min((s for s in squares if len(sol[s]) > 1),
                 key=lambda s: len(sol[s]))
        orig = sol.copy()
        for val in orig[sq]:
            assign(sol, sq, val)
            if search(sol):
                return True
            else:
                sol.update(orig)
        else:
            return False


def print_grid(grid):
    max_len = max(len(grid[s]) for s in squares if grid[s])
    for r in rows:
        for c in cols:
            print('{val:^{width}} '.format(
                val=grid[r+c] if grid[r+c] else '-',
                width=max_len), end='')
        print()


puzzle = '''4.....8.5
            .3.......
            ...7.....
            .2.....6.
            ....8.4..
            ....1....
            ...6.3.7.
            5..2.....
            1.4......'''


def parse_puzzle(puz):
    puzzle = [c if c in '123456789' else None
              for c in puz if c not in ' \n']
    assert(len(puzzle) == 81)
    return {squares[i]:puzzle[i]
            for i in range(0, len(squares))}


if __name__ == '__main__':
    with open('p096_sudoku.txt', 'r') as f:
        lines = f.read().split('\n')

    for i in range(0, len(lines), 10):
        sol = {s: '123456789' for s in squares}
        puz_str = ''.join(lines[i+1:i+10])

        puz = parse_puzzle(puz_str)
        print('Puzzle:\n')
        print_grid(puz)
        for sq, val in puz.items():
            if val:
                assign(sol, sq, val)

        if all(len(sol[s]) == 1 for s in squares):
            print('\nSolved by pure constraint propagation:\n')
        else:
            print('\nConstraint propagation result:\n')
            print_grid(sol)
            # input() # use to pause output
            search(sol)
            print('\nSearch result:\n')

        print_grid(sol)
        # input() # use to pause output
        print('\n' + '*' * 70, end='\n\n')