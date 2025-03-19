import json
from typing import Dict, Any, Optional

from starlette.websockets import WebSocket

from src.chess_board import ChessBoard
from src.decoders import Decoder
from src.encoders import Encoder
from src.enums import MessageType, Color, MessageKeys
from src.data_types import MessageDict, MoveDict, Position, Cookie, Message, \
    MoveMessage
from src.move_verifier import MoveVerifier


class ChessGameHandler:
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self.game_board: Optional[ChessBoard] = None
        self.move_verifier: MoveVerifier = MoveVerifier(self.game_board)

    def is_checkmate(self)-> bool:
        is_turn_checked: bool = self.game_board.is_white_checked \
            if self.game_board.turn == Color.WHITE else self.game_board.is_black_checked
        if not is_turn_checked:
            return False

        turn_king_position: Position = self.game_board.white_king_position\
            if self.game_board.turn == Color.WHITE else self.game_board.black_king_position
        return self.is_mate_preventable(turn_king_position)
    def is_mate_preventable(self, king_position) -> bool:
        king = self.game_board.get_piece(king_position)
        for i in range(8):
            for j in range(8):
                cur_piece = self.game_board.get_piece((i,j))
                if cur_piece is None or cur_piece.color != king.color:
                    continue
                all_valid_ends = self.move_verifier.get_all_valid_ends((i,j))
                for end in all_valid_ends:
                    if not self.move_verifier.would_leave_in_check(cur_piece, (i,j), end):
                        return True
        return False

    async def initialize_game(self, cookie: Cookie = None) -> None:
        """Initialize a new game or load from cookie."""
        board = game_state = None
        if cookie.game:
            board, game_state = Decoder.decode_game(cookie.game)
        self.game_board = ChessBoard(board=board, game_state=game_state, turn=Color.WHITE)
        msg = Encoder.encode_message(MessageType.NEW_STATE, self.game_board)
        await self.send_json(msg)

    async def restart_game(self) -> None:
        """Start a new game."""
        self.game_board = ChessBoard(turn=Color.WHITE)
        await self.send_json(Encoder.encode_message(MessageType.RESTART, self.game_board))

    async def handle_checkmate(self) -> None:
        """Handle checkmate scenario."""
        await self.send_json(Encoder.encode_message(MessageType.CHECKMATE, self.game_board))

        # Wait for user acknowledgment
        await self.websocket.receive_json()

        # Restart game
        await self.restart_game()

    async def handle_message(self, message: MessageDict) -> None:
        if message["message_type"] == str(MessageType.RESTART):
            await self.restart_game()
        elif message["message_type"] == str(MessageType.MOVE):
            await self.handle_move(MoveMessage.model_validate(message))

    async def handle_move(self, data: MoveMessage) -> None:
        """Process a move from the client."""
        start, end = Decoder.decode_move(data)

        # Handle pawn promotion
        if not self.move_verifier.is_valid_move(start, end):
            await self.send_json(Encoder.encode_message(MessageType.FAILED_MOVE, self.game_board))
            return

        elif self.move_verifier.is_final_rank_pawn(start, end):
            await self.handle_pawn_promotion(start, end)

        else:
            self.game_board.move(start, end)
            self.game_board.get_piece(end).has_moved = True
            if self.move_verifier.is_king_checked(Color.WHITE):
                self.game_board.is_white_checked = True
            if self.move_verifier.is_king_checked(Color.BLACK):
                self.game_board.is_black_checked = True


        # Update board state
        if self.game_board.is_checkmate():
            await self.handle_checkmate()
        else:
            self.game_board.change_turn()
            await self.send_json(Encoder.encode_message(MessageType.NEW_STATE, self.game_board))

    async def handle_pawn_promotion(self, start: Position, end: Position) -> None:
        """Handle pawn promotion scenario."""
        await self.send_json(Encoder.encode_message(MessageType.PROMOTION, self.game_board))

        # Wait for user selection
        message = await self.websocket.receive_json()
        promotion_piece = Decoder.decode_piece(message[MessageKeys.PIECE])
        self.game_board.move(start, end)
        self.game_board.promote_pawn(promotion_piece, end)

    async def send_json(self, data: Dict[Any, Any]) -> None:
        """Send JSON data to the client."""
        await self.websocket.send_json(data)
