from typing import List, Optional, Tuple

from src.enums import PieceType, Color
from src.piece import Piece
from src.data_types import (
    MessageDict,
    EncodedPiece,
    Position,
    EncodedBoard,
    GameState,
    KeyDecodedBoard,
    MoveDict,
)


class Decoder:
    @staticmethod
    def decode_move(move: MoveDict) -> Tuple[Position, Position]:
        start: Position =  (move["START"][0], move["START"][1])
        end: Position = (move["END"][0], move["END"][1])
        return start, end

    @staticmethod
    def decode_cookie(
        cookie: MessageDict,
    ) -> Tuple[List[List[Optional[Piece]]], GameState]:
        encoded_board: EncodedBoard = cookie.get("BOARD", None)
        game_state: GameState = {}
        key_decoded_board: KeyDecodedBoard = KeyDecodedBoard()
        for key, value in encoded_board.items():
            if key == "WHITE_KING_POSITION" or key == "BLACK_KING_POSITION":
                game_state[key] = eval(value)
            elif key == "TURN":
                game_state[key] = Color.from_string(value)
            else:
                position: Position = Decoder.decode_position(key)
                key_decoded_board[position] = value
        fully_decoded_board: List[List[Optional[Piece]]] = Decoder.decode_board(key_decoded_board)
        return fully_decoded_board, game_state

    @staticmethod
    def decode_piece(piece_dict: EncodedPiece) -> Piece:
        return Piece(
            PieceType.from_string(piece_dict["TYPE"]),
            Color.from_string(piece_dict["COLOR"]),
        )

    @staticmethod
    def decode_board(
        board_dict: KeyDecodedBoard,
    ) -> List[List[Optional[Piece]]]:
        matrix: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                current_piece_dict = board_dict.get((i, j), None)
                if current_piece_dict is not None:
                    current_piece = Decoder.decode_piece(current_piece_dict)
                    matrix[i][j] = current_piece
        return matrix

    @staticmethod
    def decode_position(position_str: str) -> Position:
        position_strs = position_str.strip("()").split(",")
        position: Position = (int(position_strs[0]), int(position_strs[1]))
        return position
