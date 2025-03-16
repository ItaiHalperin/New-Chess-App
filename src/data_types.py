from typing import Tuple, Dict, Union, TypeAlias, List

from src.enums import Color

Position: TypeAlias = Tuple[int, int]
EncodedPiece: TypeAlias = Dict[str, Union[str, bool]]
BoardValue: TypeAlias = Union[EncodedPiece, str, Position]
EncodedBoard: TypeAlias = Dict[str, BoardValue]
KeyDecodedBoard: TypeAlias = Dict[Position, EncodedPiece]
CookieBoardDict: TypeAlias = Dict[str, Union[str, EncodedPiece]]
MoveDict: TypeAlias = Dict[str, List[int]]
MessageDict: TypeAlias = Dict[str, Union[str, MoveDict, CookieBoardDict]]
GameState: TypeAlias = Dict[str, Union[Color, Position]]
