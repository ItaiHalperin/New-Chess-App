from abs_chess_board import AbsChessBoard


class MoveVerifier:
    def __init__(self, board: AbsChessBoard):
        self.board = board
    def is_valid_move(self, start_pos: tuple[int], end_pos: tuple[int]) -> bool:
        piece = self.board.get_piece(start_pos)
        if piece is None:
            return False
        # Check basic movement pattern validity
        if not self._is_valid_pattern(piece, start_pos, end_pos):
            return False

        # Check if path is clear (for pieces that can't jump)
        if not self._is_path_clear(piece, start_pos, end_pos):
            return False

        # Check if move would leave king in check
        if self._would_leave_in_check(piece, start_pos, end_pos):
            return False

        return True

    def _is_valid_pattern(self, piece, start_pos, end_pos):
        x1, y1 = start_pos
        x2, y2 = end_pos

        # Rook logic: moves horizontally or vertically
        if piece == 'ROOK':
            return x1 == x2 or y1 == y2

        # Bishop logic: moves diagonally (both x and y change equally)
        elif piece == 'BISHOP':
            return abs(x2 - x1) == abs(y2 - y1)

        # Knight logic: moves in an "L" shape (2 squares in one direction, 1 in the other)
        elif piece == 'KNIGHT':
            return (abs(x2 - x1) == 2 and abs(y2 - y1) == 1) or (abs(x2 - x1) == 1 and abs(y2 - y1) == 2)

        # Queen logic: combines the movement of both the Rook and the Bishop
        elif piece == 'QUEEN':
            return x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1)

        # King logic: moves one square in any direction
        elif piece == 'KING':
            return abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1

        # Pawn logic: moves forward one square, or two squares from its starting position; captures diagonally
        elif piece == 'PAWN':
            # Pawn movement
            if x1 == x2:
                # Moving forward by 1 square
                if y2 == y1 + 1:
                    return True
                # Moving forward by 2 squares from its starting position
                elif y1 == 1 and y2 == 3:  # Assuming pawns start at row 1
                    return True
            # Pawn captures diagonally
            elif abs(x2 - x1) == 1 and y2 == y1 + 1:
                return True

        return False  # Default: False if no match found for the piece type

    def _is_path_clear(self, piece, start_pos, end_pos):
        pass

    def _would_leave_in_check(self, piece, start_pos, end_pos):
        pass

