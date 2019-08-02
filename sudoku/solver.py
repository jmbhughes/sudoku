"""
This code is developed based on Joseph Coffland's work <https://github.com/jcoffland/fsudoku> which is
available under a GNU General Public license. You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import copy
import sys
import fileinput


class Set:
    def __init__(self, cells, indices):
        self.cells = cells
        self.indices = indices

    def unique(self):
        values = []
        for value in self.cells:
            if value in values:
                return False
            if value is not None:
                values += [value]
        return True


class Grid:
    def __init__(self, cells, size):
        self.size = size
        self.cells = cells

    def get(self, row, col):
        return self.cells[row + col * self.size]

    def set(self, row, col, value):
        self.cells[row + col * self.size] = value

    def get_row(self, row):
        return Set(map(lambda col: self.get(row, col), range(self.size)),
                   map(lambda col: row + col * self.size, range(self.size)))

    def get_column(self, col):
        return Set(map(lambda row: self.get(row, col), range(self.size)),
                   map(lambda row: row + col * self.size, range(self.size)))

    def get_block(self, blk):
        row_offset = (blk / 3) * 3
        column_offset = (blk % 3) * 3
        values = []
        indices = []
        for row in range(3):
            for col in range(3):
                r = row + row_offset
                c = col + column_offset
                values += [self.get(r, c)]
                indices += [r + c * self.size]

        return Set(values, indices)

    def iterate_sets(self):
        sets = []
        for i in range(self.size):
            sets += [self.get_row(i), self.get_column(i), self.get_block(i)]
        return sets

    def show_row(self, row):
        for col in range(self.size):
            if col and col % 3 == 0:
                sys.stdout.write(' ')
            value = self.get(row, col)
            if value is None:
                sys.stdout.write('?')
            else:
                sys.stdout.write(str(value))
            sys.stdout.write(' ')

    def show(self):
        for row in range(self.size):
            self.show_row(row)
            sys.stdout.write('\n')

            if row and row != self.size - 1 and row % 3 == 2:
                sys.stdout.write('\n')


class Puzzle:
    def __init__(self):
        size = 9
        self.grid = Grid(map(lambda x: None, range(size * size)), size)

    def is_valid(self):
        for set in self.grid.iterate_sets():
            if not set.unique():
                return False

        return True

    def assert_valid(self):
        if not self.is_valid():
            print("Puzzle invalid")
            sys.exit(1)

    def is_solved(self):
        if not self.is_valid():
            return False
        for cell in self.grid.cells:
            if cell is None:
                return False

        return True

    def show(self):
        self.grid.show()

    def read(self):
        row = 0
        for line in fileinput.input():
            nums = line.split()
            if len(nums) == 0:
                continue
            if len(nums) != self.grid.size:
                print("Invalid input at line ", row)

            for col in range(self.grid.size):
                if nums[col] == '?':
                    self.grid.set(row, col, None)
                else:
                    self.grid.set(row, col, int(nums[col]))

            row = row + 1
            if row == self.grid.size:
                break


class Possible:
    def __init__(self, value=None):
        self.possible = range(1, 10)
        self.set(value)

    def set(self, value):
        if value is None:
            self.possible = range(1, 10)
        else:
            self.possible = [value]

    def count(self):
        return len(self.possible)

    def has(self, value):
        return value in self.possible

    def remove(self, value):
        if value in self.possible:
            self.possible = filter(lambda x: x != value, self.possible)
            return True
        return False


class PossibleGrid:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.grid = Grid(map(lambda cell: Possible(cell), puzzle.grid.cells),
                         puzzle.grid.size)

    def remove_impossible(self, set):
        result = False
        values = []
        unset = []
        for cell in set.cells:
            if cell.count() == 1:
                values += [cell.possible[0]]
            else:
                unset += [cell]

        for cell in unset:
            for value in values:
                if cell.remove(value):
                    result = True
        return result


    def find_exclusives(self, set):
        exclusives = []
        values = map(lambda x: [], range(self.grid.size))

        for cell in set.cells:
            if cell.count() != 1:
                for value in cell.possible:
                    values[value - 1] += [cell]

        for i in range(self.grid.size):
            if len(values[i]) == 1:
                exclusives += (values[i][0], i + 1)

        if exclusives:
            return exclusives
        else:
            return None

    def solve(self):
        while True:
            while len(filter(lambda set: self.remove_impossible(set),
                             self.grid.iterate_sets())):
                continue

            exclusives = map(self.find_exclusives, self.grid.iterate_sets())
            exclusives = filter(lambda x: x, exclusives)
            if not exclusives:
                break
            for pair in exclusives:
                pair[0].set(pair[1])

        self.fill()

    def fill(self):
        for i in range(len(self.grid.cells)):
            if self.grid.cells[i].count() == 1:
                self.puzzle.grid.cells[i] = self.grid.cells[i].possible[0]

    def iterate_combinations(self, set, values=[]):
        results = []

        if len(values) == len(set.cells):
            return [copy.deepcopy(values)]

        cell = set.cells[len(values)]
        for value in cell.possible:
            if value not in values:
                results += self.iterate_combinations(set, values + [value])

        return results

    def try_combinations(self, puzzle, sets, index=0):
        if index == len(sets):
            self.puzzle.grid = puzzle.grid
            return

        set = sets[index]
        cpuzzle = copy.deepcopy(puzzle)

        for comb in self.iterate_combinations(set):
            valid = True

            for i in range(len(comb)):
                cindex = set.indicies[i]
                value = puzzle.grid.cells[cindex]

                if value is None:
                    cpuzzle.grid.cells[cindex] = comb[i]
                elif value != comb[i]:
                    valid = False
                    break

            if valid and cpuzzle.is_valid():
                ppuzzle = copy.deepcopy(cpuzzle)
                possible = PossibleGrid(ppuzzle)
                possible.solve()

                if ppuzzle.is_solved():
                    self.puzzle.grid = ppuzzle.grid
                    return

                elif ppuzzle.is_valid():
                    self.try_combinations(ppuzzle, sets, index + 1)

    def try_all_combinations(self):
        sets = self.grid.iterate_sets()
        self.try_combinations(copy.deepcopy(self.puzzle), sets)


def solve(puzzle):
    print("Solving . . .")
    sys.stdout.flush()
    possible = PossibleGrid(puzzle)
    possible.solve()

    if not puzzle.is_solved():
        print("hard . . .")
        sys.stdout.flush()
        possible.try_all_combinations()

    print("done")


puzzle = Puzzle()

puzzle.read()
puzzle.show()
puzzle.assert_valid()
print('-------------------')
solve(puzzle)

puzzle.show()
puzzle.assert_valid()
