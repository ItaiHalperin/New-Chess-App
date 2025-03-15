from typing import Tuple, Dict

from dict_decoders import build_matrix
from enums import Color
from src.abs_chess_board import AbsChessBoard
from src.enums import PieceType
from src.piece import Piece
from types import Position


class ChessBoard(AbsChessBoard):
    def get_board_dict(self)->Dict[str, Tuple[int, int]]:
        chess_board_dict = {"TURN": str(self.turn),
                            "WHITE_KING_POSITION": self.white_king_position,
                            "BLACK_KING_POSITION": self.black_king_position}
        for i in range(8):
            for j in range(8):
                cur_piece = self.board[i][j]
                if cur_piece is None:
                    continue
                chess_board_dict[Position(i, j)] = cur_piece.get_piece_dict()
        return chess_board_dict

    def revert_move(self, start_pos: Position, end_pos: Position, piece: Piece, prev_piece: Piece) -> None:
        self.board[start_pos[0]][start_pos[1]] = piece
        self.board[end_pos[0]][end_pos[1]] = prev_piece

    def move(self, start_pos, end_pos) -> None:
        piece = self.board[start_pos[0]][start_pos[1]]
        if piece is None:
            raise ValueError(f"'{piece}' is not a valid starting position")
        elif piece.type == PieceType.KING:
            self.black_king_position = end_pos if piece.color == Color.BLACK else self.black_king_position
            self.white_king_position = end_pos if piece.color == Color.WHITE else self.white_king_position
        self.board[end_pos[0]][end_pos[1]] = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = None

    def get_piece(self, start_pos) -> Piece:
        return self.board[start_pos[0]][start_pos[1]]

    def __init__(self, turn: Color, cookie: dict[Position, dict[str, str]] = None):
        super().__init__()
        self.board, self.white_king_position, self.white_king_position = build_matrix(cookie)
        self.turn = turn



