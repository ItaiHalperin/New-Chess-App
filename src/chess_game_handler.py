from typing import Dict, Any

from starlette.websockets import WebSocket

from src.chess_board import ChessBoard
from src.decoders import Decoder
from src.encoders import Encoder
from src.enums import MessageType, Color
from src.data_types import MessageDict, MoveDict, Position
from src.move_verifier import MoveVerifier


class ChessGameHandler:
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self.game_board: ChessBoard = ChessBoard()
        self.move_verifier: MoveVerifier = MoveVerifier(self.game_board)

    async def initialize_game(self, cookie: MessageDict = None) -> None:
        """Initialize a new game or load from cookie."""
        board = game_state = None
        if cookie:
            board, game_state = Decoder.decode_cookie(cookie)
        self.game_board = ChessBoard(board=board, game_state=game_state)
        await self.send_json(Encoder.encode_message(MessageType.NEW_STATE, self.game_board))

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

    async def handle_move(self, data: MoveDict, ) -> None:
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
        encoded_promotion_piece = await self.websocket.receive_json()
        promotion_piece = Decoder.decode_piece(encoded_promotion_piece)
        self.game_board.move(start, end)
        self.game_board.promote_pawn(promotion_piece, end)

    async def send_json(self, data: Dict[Any, Any]) -> None:
        """Send JSON data to the client."""
        await self.websocket.send_json(data)
