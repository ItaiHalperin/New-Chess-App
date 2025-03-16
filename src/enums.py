from enum import Enum, auto
from typing import Self


class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, name: str) -> Self:
        try:
            return cls[name]  # Lookup enum by name
        except KeyError:
            raise ValueError(f"'{name}' is not a valid ChessPiece")


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, name: str) -> Self:
        try:
            return cls[name]  # Lookup enum by name
        except KeyError:
            raise ValueError(f"'{name}' is not a valid Color")


class MessageType(Enum):
    STARTUP = auto()
    MOVE_SELECTED = auto()
    BOARD_UPDATE = auto()
    RESTART = auto()
    NEW_STATE = auto()
    CHECKMATE = auto()
    FAILED_MOVE = auto()
    PROMOTION = auto()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, name: str) -> Self:
        try:
            return cls[name]  # Lookup enum by name
        except KeyError:
            raise ValueError(f"'{name}' is not a valid MessageType")
