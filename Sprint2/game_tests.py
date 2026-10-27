import unittest
from board_logic import SolitaireLogic

class TestSolitaireLogic(unittest.TestCase):

    def test_choose_board_size_and_type(self):
        game = SolitaireLogic(size=5, board_type="Diamond")
        self.assertEqual(game.size, 5)
        self.assertEqual(game.board_type, "Diamond")

    def test_start_new_game(self):
        game = SolitaireLogic(size=7, board_type="English")
        center = 3
        # Center should be empty (0)
        self.assertEqual(game.board[center][center], 0)
        # Non-center positions in valid areas should have pegs (1)
        self.assertEqual(game.board[3][1], 1)

    def test_making_a_move(self):
        game = SolitaireLogic(size=7, board_type="English")
        # Perform a valid move
        result = game.make_move((3, 1), (3, 3))
        self.assertTrue(result)
        self.assertEqual(game.board[3][1], 0)
        self.assertEqual(game.board[3][2], 0)
        self.assertEqual(game.board[3][3], 1)

    def test_checking_end_of_game(self):
        game = SolitaireLogic(size=3, board_type="English")
        # Clear the board so no moves are possible
        for r in range(3):
            for c in range(3):
                game.board[r][c] = 0
        
        has_moves = game.has_any_moves()
        self.assertFalse(has_moves)

if __name__ == '__main__':
    unittest.main()