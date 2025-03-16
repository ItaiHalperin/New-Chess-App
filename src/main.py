import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.chess_game_handler import ChessGameHandler
from src.encoders import Encoder
from src.enums import MessageType
from src.data_types import MessageDict

# Constants
DEFAULT_PORT = 8000
INDEX_PATH = "../index.html"
STATIC_PATH = "/Users/itaihalperin/chess/static"

# Initialize FastAPI app
app = FastAPI()

# Setup static files
static_directory = Path("../static").resolve()
app.mount("/static", StaticFiles(directory=static_directory), name="static")


# Routes
@app.get("/")
async def get() -> HTMLResponse:
    """Serve the main HTML page."""
    html_content = Path(INDEX_PATH).read_text()
    return HTMLResponse(html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint for game communication."""
    await websocket.accept()

    # Create game handler
    game_handler = ChessGameHandler(websocket)

    # Initial startup message
    await websocket.send_json(Encoder.encode_message(message_type=MessageType.STARTUP))

    # Handle cookie
    cookie: MessageDict = await websocket.receive_json()
    await game_handler.initialize_game(cookie)

    # Main game loop
    while True:
        if game_handler.game_board.is_checkmate():
            await game_handler.handle_checkmate()
        else:
            data = await websocket.receive_json()
            await game_handler.handle_move(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    uvicorn.run(app, host="0.0.0.0", port=port)
