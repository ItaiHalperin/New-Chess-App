from typing import Tuple

from dict_decoder import build_matrix
from enums import Color
from types import Position


class ChessBoard:
    def __init__(self, turn: Color, cookie: dict[Position, dict[str, str]] = None):
        self.board = build_matrix(cookie)
        self.turn = turn

