import unittest
from queue import Queue

from Puissance4_RUNSER_KOHLER import Board, alpha_beta_decision


class BoardTest(unittest.TestCase):
    def test_new_board_is_empty(self):
        board = Board()

        self.assertEqual(0, board.grid.sum())
        self.assertEqual([3, 4, 2, 5, 1, 6, 0], board.get_possible_moves())

    def test_disks_stack_from_the_bottom(self):
        board = Board()

        self.assertTrue(board.add_disk(3, 1, update_display=False))
        self.assertTrue(board.add_disk(3, 2, update_display=False))

        self.assertEqual(1, board.grid[3][0])
        self.assertEqual(2, board.grid[3][1])

    def test_horizontal_victory(self):
        board = Board()
        for column in range(4):
            board.grid[column][0] = 1

        self.assertTrue(board.check_victory())

    def test_vertical_victory(self):
        board = Board()
        for row in range(4):
            board.grid[2][row] = 2

        self.assertTrue(board.check_victory())

    def test_diagonal_victory(self):
        board = Board()
        for offset in range(4):
            board.grid[offset][offset] = 1

        self.assertTrue(board.check_victory())

    def test_board_copy_is_independent(self):
        board = Board()
        copied_board = board.copy()

        copied_board.grid[0][0] = 1

        self.assertEqual(0, board.grid[0][0])
        self.assertEqual(1, copied_board.grid[0][0])

    def test_alpha_beta_returns_a_legal_move(self):
        board = Board()
        result = Queue()

        alpha_beta_decision(
            board=board,
            turn=1,
            ai_level=1,
            queue=result,
            player=1,
        )

        self.assertIn(result.get_nowait(), board.get_possible_moves())


if __name__ == "__main__":
    unittest.main()
