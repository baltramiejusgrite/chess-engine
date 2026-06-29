import chess
import chess.engine
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.search import choose_move
from app.engines_config import find_stockfish

app = FastAPI(title="Chess Engine")

STOCKFISH_PATH = find_stockfish()


class MoveRequest(BaseModel):
    fen: str
    difficulty: str = "my_engine"  # default to your own engine


def get_stockfish_move(board: chess.Board, skill_level: int) -> chess.Move:
    """Get a move from Stockfish at a given skill level."""
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    try:
        engine.configure({"Skill Level": skill_level})
        result = engine.play(board, chess.engine.Limit(time=0.3))
        return result.move
    finally:
        engine.quit()


# Map difficulty labels to how we generate the move
DIFFICULTY_SETTINGS = {
    "my_engine": None,        # your own engine
    "stockfish_easy": 1,      # ~1100
    "stockfish_medium": 5,    # ~1600
    "stockfish_hard": 10,     # ~2100
    "stockfish_max": 20,      # full strength
}


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.post("/move")
def get_engine_move(req: MoveRequest):
    board = chess.Board(req.fen)

    if board.is_game_over():
        return {"game_over": True, "result": board.result()}

    skill = DIFFICULTY_SETTINGS.get(req.difficulty, None)

    if skill is None:
        # Use your own engine
        move = choose_move(board, depth=5)
    else:
        # Use Stockfish at the chosen skill level
        move = get_stockfish_move(board, skill)

    board.push(move)

    return {
        "move": move.uci(),
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    }