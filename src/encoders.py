from typing import Union, Dict
from src.chess_board import ChessBoard
from src.enums import MessageType
from src.data_types import EncodedBoard, EncodedPiece, GameState, Game, Cookie
from src.piece import Piece


class Encoder:
    @staticmethod
    def encode_piece(piece: Piece) -> EncodedPiece:
        return EncodedPiece(color=str(piece.color), type=str(piece.type), has_moved=piece.has_moved)

    @staticmethod
    def encode_game(chess_board: ChessBoard) -> Game:
        game_state: GameState = GameState(white_king_position=chess_board.white_king_position,
                                            black_king_position=chess_board.black_king_position,
                                            is_white_checked=chess_board.is_white_checked,
                                            is_black_checked=chess_board.is_black_checked,
                                            turn=chess_board.turn,)

        board_dict = {}
        for i in range(8):
            for j in range(8):
                cur_piece = chess_board.board[i][j]
                if cur_piece is None:
                    continue
                position_str: str = str((i, j))
                board_dict[position_str] = Encoder.encode_piece(cur_piece)
        return Game(game_state=game_state, board=board_dict)

    @staticmethod
    def encode_message(
        message_type: MessageType, chess_board: ChessBoard = None
    ) -> Dict[str, Union[str, EncodedBoard]]:
        if message_type == MessageType.STARTUP:
            return {"message_type": str(message_type)}
        else:
            game = Encoder.encode_game(chess_board)
            return Cookie(message_type=str(message_type), game=game).model_dump()
