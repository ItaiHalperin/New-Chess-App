from enum import Enum, auto
from typing import Self


class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()
    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, name: str)-> Self:
        try:
            return cls[name]  # Lookup enum by name
        except KeyError:
            raise ValueError(f"'{name}' is not a valid ChessPiece")


class Color(Enum):
    WHITE = auto()
    BLACK = auto()
    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, name: str)-> Self:
        try:
            return cls[name]  # Lookup enum by name
        except KeyError:
            raise ValueError(f"'{name}' is not a valid Color")