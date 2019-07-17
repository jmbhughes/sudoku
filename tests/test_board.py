from sudoku.board import SquareBoard
import pytest


class TestSquareBoard:
    def test_init(self):
        """
        Confirm that a SquareBoard is properly initialized
        """

        # Check that a perfect square board can be created and that the size is correct
        sizes = [4, 9, 16]
        for size in sizes:
            board = SquareBoard(size)
            assert board.size == size, "Board size not saved properly"
            assert board.grid.shape == (size, size), "Grid not initialized properly"

        # Check if boards that aren't perfect squares are excluded
        with pytest.raises(ValueError):
            SquareBoard(3)

    def test_see(self):
        board = SquareBoard(4)
        board.grid[0, 1] = 2
        assert board.see(1, 2) == 2, "Not properly seeing a stored value"

    def test_fill(self):
        board = SquareBoard(16)
        board.fill(1, 1, 5)
        assert board.see(1, 1) == 5

