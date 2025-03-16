from typing import Tuple, List, Optional

from enums import Color
from src.abs_chess_board import AbsChessBoard
from src.enums import PieceType
from src.piece import Piece
from src.data_types import Position, GameState


class ChessBoard(AbsChessBoard):
    def promote_pawn(self, promotion_piece: Piece, position: Position) -> None:
        self.board[position[0]][position[1]] = promotion_piece

    def revert_move(
        self,
        start_pos: Position,
        end_pos: Position,
        piece: Piece,
        prev_piece: Piece,
    ) -> None:
        self.board[start_pos[0]][start_pos[1]] = piece
        self.board[end_pos[0]][end_pos[1]] = prev_piece

    def move(self, start_pos: Position, end_pos: Position) -> None:
        piece = self.board[start_pos[0]][start_pos[1]]
        if piece is None:
            raise ValueError(f"'{piece}' is not a valid starting position")
        elif piece.type == PieceType.KING:
            self.black_king_position: Position = end_pos if piece.color == Color.BLACK else self.black_king_position
            self.white_king_position: Position = end_pos if piece.color == Color.WHITE else self.white_king_position
        self.board[end_pos[0]][end_pos[1]] = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = None

    def get_piece(self, start_pos: Position) -> Piece:
        return self.board[start_pos[0]][start_pos[1]]

    def change_turn(self) -> None:
        self.turn: Color = Color.WHITE if self.turn == Color.BLACK else Color.BLACK

    def __init__(
        self,
        turn: Optional[Color] = None,
        board: Optional[List[List[Optional[Piece]]]] = None,
        game_state: Optional[GameState] = None,
    ) -> None:
        super().__init__()
        if board is None:
            if turn is None:
                raise ValueError(f"'{turn}' is not a valid Turn for default chess board")
            self.board, self.white_king_position, self.white_king_position = ChessBoard.default_board()
            self.turn = turn
        elif game_state is not None:
            self.board = board
            self.white_king_position = game_state["WHITE_KING_POSITION"]
            self.black_king_position = game_state["BLACK_KING_POSITION"]
            self.turn = game_state["TURN"]

    @staticmethod
    def default_board() -> Tuple[List[List[Optional[Piece]]], Position, Position]:
        matrix: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        matrix[0][0] = Piece(PieceType.ROOK, Color.WHITE)
        matrix[0][1] = Piece(PieceType.KNIGHT, Color.WHITE)
        matrix[0][2] = Piece(PieceType.BISHOP, Color.WHITE)
        matrix[0][3] = Piece(PieceType.QUEEN, Color.WHITE)
        matrix[0][4] = Piece(PieceType.KING, Color.WHITE)
        white_king_position = (0, 4)
        matrix[0][5] = Piece(PieceType.BISHOP, Color.WHITE)
        matrix[0][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        matrix[0][7] = Piece(PieceType.ROOK, Color.WHITE)

        # Second row (white pawns)
        for i in range(8):
            matrix[1][i] = Piece(PieceType.PAWN, Color.WHITE)

        # Middle rows (empty spaces)
        for i in range(2, 6):
            for j in range(8):
                matrix[i][j] = None  # or however you represent empty spaces

        # Seventh row (black pawns)
        for i in range(8):
            matrix[6][i] = Piece(PieceType.PAWN, Color.BLACK)

        # Eighth row (black pieces)
        matrix[7][0] = Piece(PieceType.ROOK, Color.BLACK)
        matrix[7][1] = Piece(PieceType.KNIGHT, Color.BLACK)
        matrix[7][2] = Piece(PieceType.BISHOP, Color.BLACK)
        matrix[7][3] = Piece(PieceType.QUEEN, Color.BLACK)
        matrix[7][4] = Piece(PieceType.KING, Color.BLACK)
        black_king_position = (7, 4)
        matrix[7][5] = Piece(PieceType.BISHOP, Color.BLACK)
        matrix[7][6] = Piece(PieceType.KNIGHT, Color.BLACK)
        matrix[7][7] = Piece(PieceType.ROOK, Color.BLACK)
        return matrix, white_king_position, black_king_position
