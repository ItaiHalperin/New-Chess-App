from typing import List, Optional, Tuple
from piece import Piece, PieceType
from enums import Color
from types import Position


def build_matrix(cookie: dict[Position, dict[str, str]] = None) -> Tuple[List[List[Optional[Piece]]], Position, Position]:
    matrix: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
    white_king_pos = (-1, -1)
    black_king_pos = (-1, -1)
    if cookie is None:
        matrix[0][0] = Piece(PieceType.ROOK, Color.WHITE)
        matrix[0][1] = Piece(PieceType.KNIGHT, Color.WHITE)
        matrix[0][2] = Piece(PieceType.BISHOP, Color.WHITE)
        matrix[0][3] = Piece(PieceType.QUEEN, Color.WHITE)
        matrix[0][4] = Piece(PieceType.KING, Color.WHITE)
        white_king_pos = (0, 4)
        matrix[0][5] = Piece(PieceType.BISHOP, Color.WHITE)
        matrix[0][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        matrix[0][7] = Piece(PieceType.ROOK, Color.WHITE)

        # Second row (white pawns)
        for i in range(8):
            matrix[1][i] = Piece(PieceType.PAWN, Color.WHITE)

        # Middle rows (empty spaces)
        for i in range(2, 6):
            for j in range(8):
                matrix[i][j] = None  # or however you represent empty spaces

        # Seventh row (black pawns)
        for i in range(8):
            matrix[6][i] = Piece(PieceType.PAWN, Color.BLACK)

        # Eighth row (black pieces)
        matrix[7][0] = Piece(PieceType.ROOK, Color.BLACK)
        matrix[7][1] = Piece(PieceType.KNIGHT, Color.BLACK)
        matrix[7][2] = Piece(PieceType.BISHOP, Color.BLACK)
        matrix[7][3] = Piece(PieceType.QUEEN, Color.BLACK)
        matrix[7][4] = Piece(PieceType.KING, Color.BLACK)
        black_king_pos = (7, 4)
        matrix[7][5] = Piece(PieceType.BISHOP, Color.BLACK)
        matrix[7][6] = Piece(PieceType.KNIGHT, Color.BLACK)
        matrix[7][7] = Piece(PieceType.ROOK, Color.BLACK)

    else:
        for i in range(8):
            for j in range(8):
                current_piece = cookie.get((i, j), None)
                if current_piece is not None:
                    piece_type = PieceType.from_string(current_piece.get("PieceType", None))
                    piece_color = Color.from_string(current_piece.get("Color", None))
                    white_king_pos = (i, j) if piece_type == "KING" and piece_color == "WHITE" else white_king_pos
                    black_king_pos = (i, j) if piece_type == "KING" and piece_color == "BLACK" else black_king_pos
                    matrix[i][j] = Piece(piece_type, piece_color)

    return matrix, white_king_pos, black_king_pos