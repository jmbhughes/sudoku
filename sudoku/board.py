import numpy as np
import math


class SquareBoard:
    def __init__(self, size: int) -> None:
        """
        Initialize a square board

        A 16x16 square board would have 16 symbols, be 16x16 cells, and have 4x4 blocks

        Note: 0 is used as empty square in this implementation

        :param size: how wide and tall the board is, must be a perfect square. It also dictates how many
            symbols there are.
        """

        # Check that the input size is a perfect square
        def is_square(integer: int) -> bool:
            root = math.sqrt(integer)
            return integer == int(root + 0.5) ** 2

        if not is_square(size):
            raise ValueError("The size must be a perfect square")

        self.size = size

        # Set up the internal state as a numpy array, zero means an empty square
        self.grid = np.zeros((self.size, self.size), dtype=int)

    def check_solved(self) -> bool:
        """
        Check if the board has been properly solved.
        :return: whether the board is completely solved
        """
        block_size = int(np.sqrt(self.size))  # how big each block is, the square root of the size
        for i in range(self.size):
            # j, k index top left hand corner of each block_size x block_size tile
            j, k = (i // block_size) * block_size, (i % block_size) * block_size
            if len(set(self.grid[i, :])) != self.size or len(set(self.grid[:, i])) != self.size \
                    or len(set(self.grid[j:j + block_size, k:k + block_size].ravel())) != self.size:
                return False
        return True

    def _in_bounds(self, x: int, y: int) -> bool:
        """
        Checks if the requested location is in the grid
        :param x:
        :param y:
        :return:
        """
        return 0 <= x - 1 < self.size and 0 <= y - 1 < self.size

    def see(self, x: int, y: int) -> int:
        """
        Peeks at stored value in the Sudoku grid
        :param x:
        :param y:
        :return: value at (x, y)
        """
        assert self._in_bounds(x, y), "Coordinates ({}, {}) are out of grid.".format(x, y)
        return self.grid[x-1, y-1]

    def fill(self, x: int, y: int, value: int) -> None:
        """
        Update the entry in a cell. Bottom-left is (1,1) and upper right is (size, size)
        :param x: The horizontal location of the cell.
        :param y: The vertical location of the cell
        :param value: The value to add in the (x,y) cell. This value must satisfy 0 <= value <= size of grid
        """
        assert self._in_bounds(x, y), "Coordinates ({}, {}) are out of grid.".format(x, y)
        if 0 <= value <= self.size:
            self.grid[x-1, y-1] = value
        else:
            raise ValueError("Attempting to insert an invalid value.")

    def __str__(self) -> str:
        """
        :return: simple string representation of grid
        """
        return str(self.grid)


class StandardBoard(SquareBoard):
    def _init__(self):
        super().__init__(9)
