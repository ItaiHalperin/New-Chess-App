from abs_chess_board import AbsChessBoard
from src.enums import PieceType, Color
from src.piece import Piece
from src.types import Position


class MoveVerifier:
    def __init__(self, board: AbsChessBoard):
        self.board = board
    def is_valid_move(self, start_pos: Position, end_pos: Position) -> bool:
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

    def _is_valid_pattern(self, piece: Piece, start_pos: Position, end_pos: Position) -> bool:
        x1, y1 = start_pos
        x2, y2 = end_pos

        # Rook logic: moves horizontally or vertically
        if piece.type == PieceType.ROOK:
            return x1 == x2 or y1 == y2

        # Bishop logic: moves diagonally (both x and y change equally)
        elif piece.type == PieceType.BISHOP:
            return abs(x2 - x1) == abs(y2 - y1)

        # Knight logic: moves in an "L" shape (2 squares in one direction, 1 in the other)
        elif piece.type == PieceType.KNIGHT:
            return (abs(x2 - x1) == 2 and abs(y2 - y1) == 1) or (abs(x2 - x1) == 1 and abs(y2 - y1) == 2)

        # Queen logic: combines the movement of both the Rook and the Bishop
        elif piece.type == PieceType.QUEEN:
            return x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1)

        # King logic: moves one square in any direction
        elif piece.type == PieceType.KING:
            return abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1

        # Pawn logic: moves forward one square, or two squares from its starting position; captures diagonally
        elif piece.type == PieceType.PAWN:
            # Pawn movement
            if x1 == x2:
                # Moving forward by 1 square
                if y2 == y1 + 1 and piece.color == Color.WHITE:
                    return True
                elif y2 == y1 - 1 and piece.color == Color.BLACK:
                    return True
                # Moving forward by 2 squares from its starting position
                elif y1 == 1 and y2 == 3 and piece.color == Color.WHITE:
                    return True
                elif y1 == 6 and y2 == 4 and piece.color == Color.BLACK:
                    return True
            # Pawn captures diagonally
            else:
                end_piece = self.board.get_piece(end_pos)
                if abs(x2 - x1) != 1 or end_piece is None:
                    return False
                elif y2 == y1 + 1 and piece.color == Color.WHITE and end_piece.color == Color.BLACK:
                    return True
                elif y2 == y1 - 1 and piece.color == Color.BLACK and end_piece.color == Color.WHITE:
                    return True

        return False  # Default: False if no match found for the piece type

    def _is_path_clear(self, piece: Piece, start_pos: Position, end_pos: Position) -> bool:
        end_piece = self.board.get_piece(end_pos)
        if end_piece is not None and (end_piece.color == piece.color or piece.type == PieceType.PAWN):
            return False
        x1, y1 = start_pos
        x2, y2 = end_pos
        if piece.type == PieceType.KNIGHT:
            end_piece = self.board.get_piece(end_pos)
            return end_piece is None or end_piece.color != piece.color
        x_dir = 1 if x1 < x2 else -1 if x1 > x2 else 0
        y_dir = 1 if y1 < y2 else -1 if y1 > y2 else 0
        x, y = x1 + x_dir, y1 + y_dir
        while (x, y) != end_pos:
            cur_piece = self.board.get_piece(Position(x,y))
            if cur_piece is not None:
                return False
            x, y = x + x_dir, y + y_dir
        return True

    def _would_leave_in_check(self, piece, start_pos, end_pos) -> bool:
        end_piece = self.board.get_piece(end_pos)
        self.board.move(start_pos, end_pos)
        king_color = piece.color
        king_position = self.board.white_king_position if king_color == Color.WHITE else self.board.black_king_position
        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):
                if x_dir == 0 and y_dir == 0:
                    continue
                if not self._is_direction_safe(king_color, king_position, x_dir, y_dir):
                    self.board.revert_move(start_pos, end_pos, piece, end_piece)
                    return True
        if self._is_threatened_by_knight(king_color, king_position):
            self.board.revert_move(start_pos, end_pos, piece, end_piece)
            return True
        self.board.revert_move(start_pos, end_pos, piece, end_piece)
        return False

    def _is_direction_safe(self, king_color: Color, king_position: Position, x_dir: int, y_dir: int) -> bool:
        x, y = king_position[0] + x_dir, king_position[1] + y_dir
        while 0 <= x <= 7 and 0 <= y <= 7:
            cur_piece = self.board.get_piece(Position(x,y))
            if cur_piece is None:
                x += x_dir
                y += y_dir
            elif cur_piece.color != king_color:
                return self._is_valid_pattern(cur_piece, Position(x,y), king_position)
            else:
                return True
        return True

    def _is_threatened_by_knight(self, king_color: Color, king_position: Position) -> bool:
        knight_offsets = [(i, j) for i in [-2, -1, 1, 2] for j in [-2, -1, 1, 2] if abs(i) + abs(j) == 3]

        # Get coordinates of the king
        king_x, king_y = king_position

        # Check all possible knight positions that could threaten the king
        for offset_x, offset_y in knight_offsets:
            x, y = king_x + offset_x, king_y + offset_y

            # Check if position is within board boundaries
            if 0 <= x <= 7 and 0 <= y <= 7:
                piece = self.board.get_piece(Position(x, y))

                # If there's a knight of the opposite color at this position, the king is threatened
                if (piece is not None and
                        piece.type == PieceType.KNIGHT and
                        piece.color != king_color):
                    return True

        # No threatening knights found
        return False

