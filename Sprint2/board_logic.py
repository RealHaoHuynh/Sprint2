class SolitaireLogic:
    def __init__(self, size=7, board_type="English"):
        self.size = size
        self.board_type = board_type
        self.board = []
        self.is_game_over = False
        self.initialize_board()

    def initialize_board(self):
        # Create a 2D grid initialized to -1 (invalid spaces)
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        center = self.size // 2

        for r in range(self.size):
            for c in range(self.size):
                if self.board_type == "English":
                    # English peg solitaire board layout (cross shape)
                    arm = self.size // 3
                    offset = (self.size - arm) // 2
                    if (offset <= r < self.size - offset) or (offset <= c < self.size - offset):
                        self.board[r][c] = 1
                elif self.board_type == "Diamond":
                    if abs(r - center) + abs(c - center) <= center:
                        self.board[r][c] = 1
                elif self.board_type == "Hexagon":
                    if abs(r - center) + abs(c - center) <= center + 1:
                        self.board[r][c] = 1

        # Center hole is empty at start
        if 0 <= center < self.size and 0 <= center < self.size:
            if self.board[center][center] == 1:
                self.board[center][center] = 0

        self.is_game_over = False

    def make_move(self, start_pos, end_pos):
        r1, c1 = start_pos
        r2, c2 = end_pos

        if not self.check_valid_move(r1, c1, r2, c2):
            return False

        # Find middle peg position to remove it
        mid_r = (r1 + r2) // 2
        mid_c = (c1 + c2) // 2

        self.board[r1][c1] = 0
        self.board[mid_r][mid_c] = 0
        self.board[r2][c2] = 1

        # Check if any moves are left
        if not self.has_any_moves():
            self.is_game_over = True

        return True

    def check_valid_move(self, r1, c1, r2, c2):
        # Bounds check
        if not (0 <= r1 < self.size and 0 <= c1 < self.size):
            return False
        if not (0 <= r2 < self.size and 0 <= c2 < self.size):
            return False

        # Start must have a peg, end must be empty
        if self.board[r1][c1] != 1 or self.board[r2][c2] != 0:
            return False

        # Must jump exactly 2 spaces horizontally or vertically
        row_diff = abs(r1 - r2)
        col_diff = abs(c1 - c2)
        if not ((row_diff == 2 and col_diff == 0) or (row_diff == 0 and col_diff == 2)):
            return False

        # Middle position must contain a peg
        mid_r = (r1 + r2) // 2
        mid_c = (c1 + c2) // 2
        if self.board[mid_r][mid_c] != 1:
            return False

        return True

    def has_any_moves(self):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 1:
                    for dr, dc in directions:
                        if self.check_valid_move(r, c, r + dr, c + dc):
                            return True
        return False