from typing import Tuple, Dict, Union, TypeAlias, List, Self
from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Optional


class EncodedPiece(BaseModel):
    color: str
    type: str
    has_moved: bool

Position: TypeAlias = Tuple[int, int]
BoardValue: TypeAlias = Union[EncodedPiece, str, Position]
EncodedBoard: TypeAlias = Dict[str, BoardValue]
KeyDecodedBoard: TypeAlias = Dict[Position, EncodedPiece]
CookieBoardDict: TypeAlias = Dict[str, Union[str, EncodedPiece]]
MoveDict: TypeAlias = Dict[str, List[int]]
MessageDict: TypeAlias = Dict[str, Union[str, MoveDict, CookieBoardDict]]

class Message(BaseModel):
    message_type: str

class Move(BaseModel):
    start_position: Position
    end_position: Position

class MoveMessage(Message):
    move: Move

class GameState(BaseModel):
    white_king_position: Position
    black_king_position: Position
    turn: str
    is_white_checked: bool
    is_black_checked: bool

class Game(BaseModel):
    game_state: GameState
    board: EncodedBoard

class Cookie(Message):
    message_type: str
    game: Game