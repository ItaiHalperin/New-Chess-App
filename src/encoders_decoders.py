from typing import Dict

from src.chess_board import ChessBoard
from src.enums import MessageType


class Encoder:
    @staticmethod
    def encode_message(message_type: MessageType, chess_board: ChessBoard=None) -> Dict[str, str]:
        if message_type == MessageType.STARTUP:
            return {"MESSAGE_TYPE": str(message_type)}
        else:
            return {"MESSAGE_TYPE": str(message_type), "BOARD": chess_board.get_board_dict()}
