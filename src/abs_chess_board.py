from abc import ABC, abstractmethod
from typing import Optional, List

from src.enums import Color
from src.piece import Piece
from src.data_types import Position


class AbsChessBoard(ABC):
    def __init__(self) -> None:
        self.black_king_position: Optional[Position] = None
        self.white_king_position: Optional[Position] = None
        self.turn: Optional[Color] = None
        self.board: Optional[List[List[Optional[Piece]]]] = None
        self.is_white_checked: bool = False
        self.is_black_checked: bool = False

    @abstractmethod
    def get_piece(self, pos: Position) -> Piece:
        pass

    @abstractmethod
    def move(self, start_pos: Position, end_pos: Position) -> None:
        pass

    @abstractmethod
    def revert_move(
        self,
        start_pos: Position,
        end_pos: Position,
        piece: Piece,
        prev_piece: Piece,
    ) -> None:
        pass
