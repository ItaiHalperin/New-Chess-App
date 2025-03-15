from abc import ABC


class AbsChessBoard(ABC):
    def __init__(self):
        self.turn = None
        self.board = None

    def get_piece(self, start_pos):
        pass