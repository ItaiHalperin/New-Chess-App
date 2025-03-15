from abc import ABC, abstractmethod

from src.piece import Piece
from src.types import Position


class AbsChessBoard(ABC):
    def __init__(self):
        self.black_king_position = None
        self.white_king_position = None
        self.turn = None
        self.board = None
    @abstractmethod
    def get_piece(self, pos):
        pass
    @abstractmethod
    def move(self, start_pos, end_pos):
        pass
    @abstractmethod
    def revert_move(self, start_pos: Position, end_pos: Position, piece: Piece, prev_piece: Piece):
        pass