from typing import Union, Dict

from src.chess_board import ChessBoard
from src.enums import MessageType
from src.data_types import EncodedBoard, EncodedPiece, Position
from src.piece import Piece


class Encoder:
    @staticmethod
    def encode_piece(piece: Piece) -> EncodedPiece:
        return {
            "COLOR": str(piece.color),
            "TYPE": str(piece.type),
            "HAS_MOVED": piece.has_moved,
        }

    @staticmethod
    def encode_board(chess_board: ChessBoard, with_game_state: bool = False) -> EncodedBoard:
        if with_game_state:
            chess_board_dict = {
                "TURN": chess_board.turn,
                "WHITE_KING_POSITION": chess_board.white_king_position,
                "BLACK_KING_POSITION": chess_board.black_king_position,
            }
        else:
            chess_board_dict = {}
        for i in range(8):
            for j in range(8):
                cur_piece = chess_board.board[i][j]
                if cur_piece is None:
                    continue
                chess_board_dict[str(Position(i, j))] = Encoder.encode_piece(cur_piece)
        return chess_board_dict

    @staticmethod
    def encode_message(
        message_type: MessageType, chess_board: ChessBoard = None
    ) -> Dict[str, Union[str, EncodedBoard]]:
        if message_type == MessageType.STARTUP:
            return {"MESSAGE_TYPE": str(message_type)}
        else:
            board_dict = Encoder.encode_board(chess_board, with_game_state=True)
            return {"MESSAGE_TYPE": str(message_type), "BOARD": board_dict}
