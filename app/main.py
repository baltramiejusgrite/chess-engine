import chess
import chess.engine
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.search import choose_move
from app.engines_config import find_stockfish

app = FastAPI(title="Chess Engine")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

STOCKFISH_PATH = find_stockfish()


class MoveRequest(BaseModel):
    fen: str
    difficulty: str = "my_engine_3"


def get_stockfish_move(board: chess.Board, skill_level: int) -> chess.Move:
    """Get a move from Stockfish at a given skill level (0-20)."""
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    try:
        engine.configure({"Skill Level": skill_level})
        result = engine.play(board, chess.engine.Limit(time=0.3))
        return result.move
    finally:
        engine.quit()


DIFFICULTY_SETTINGS = {
    "my_engine_1": ("engine", 2),
    "my_engine_2": ("engine", 3),
    "my_engine_3": ("engine", 5),
    "stockfish_4": ("stockfish", 8),
    "magnus":      ("stockfish", 17),
    "stockfish_6": ("stockfish", 20),
}


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.post("/move")
def get_engine_move(req: MoveRequest):
    board = chess.Board(req.fen)

    if board.is_game_over():
        return {"game_over": True, "result": board.result()}

    setting = DIFFICULTY_SETTINGS.get(req.difficulty, ("engine", 5))
    kind, value = setting

    if kind == "engine":
        move = choose_move(board, depth=value)
    else:
        move = get_stockfish_move(board, value)

    board.push(move)

    return {
        "move": move.uci(),
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    }