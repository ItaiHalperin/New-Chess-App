import json
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
    MoveDict, Game, Move, MoveMessage,
)


class Decoder:
    @staticmethod
    def decode_move(move_message: MoveMessage) -> Tuple[Position, Position]:
        start: Position =  (move_message.move.start_position[0], move_message.move.start_position[1])
        end: Position = (move_message.move.end_position[0], move_message.move.end_position[1])
        return start, end

    @staticmethod
    def decode_game(
        game: Game,
    ) -> Tuple[List[List[Optional[Piece]]], GameState]:
        encoded_board: EncodedBoard = game.board
        encoded_game_state: GameState = game.game_state
        key_decoded_board: KeyDecodedBoard = {}
        for key, value in encoded_board.items():
            position: Position = Decoder.decode_position(key)
            key_decoded_board[position] = value
        fully_decoded_board: List[List[Optional[Piece]]] = Decoder.decode_board(key_decoded_board)
        return fully_decoded_board, encoded_game_state

    @staticmethod
    def decode_piece(piece_dict: EncodedPiece) -> Piece:
        return Piece(
            PieceType.from_string(piece_dict.type.upper()),
            Color.from_string(piece_dict.color.upper()),
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

    @staticmethod
    def recursive_json_loads(data):
        """
        Recursively applies json.loads to a string, layer by layer.

        Args:
            data: A string that may contain nested JSON strings.

        Returns:
            The fully parsed Python object, or the original input if no valid JSON
            is found at any level.
        """
        if isinstance(data, str):
            try:
                loaded_data = json.loads(data)
                if isinstance(loaded_data, (dict, list)):
                    return Decoder._process_loaded_data(loaded_data)
                else:
                    return loaded_data
            except json.JSONDecodeError:
                return data
        elif isinstance(data, dict):
            return Decoder._process_loaded_data(data)
        elif isinstance(data, list):
            return Decoder._process_loaded_data(data)
        else:
            return data

    @staticmethod
    def _process_loaded_data(loaded_data):
        """
        Helper function to process a loaded JSON object (dict or list).
        """
        if isinstance(loaded_data, dict):
            return {k: Decoder.recursive_json_loads(v) for k, v in loaded_data.items()}
        elif isinstance(loaded_data, list):
            return [Decoder.recursive_json_loads(item) for item in loaded_data]
        return loaded_data