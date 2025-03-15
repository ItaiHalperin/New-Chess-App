from enum import Enum, auto

from enums import PieceType, Color


class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False
    def get_piece_dict(self):
        return {"COLOR": str(self.color), "TYPE": str(self.type), "HAS_MOVED": self.has_moved}