import chess
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.engine import choose_move

app = FastAPI(title="Chess Engine")


class MoveRequest(BaseModel):
    fen: str


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.post("/move")
def get_engine_move(req: MoveRequest):
    board = chess.Board(req.fen)
    if board.is_game_over():
        return {"game_over": True, "result": board.result()}
    move = choose_move(board)
    board.push(move)
    return {
        "move": move.uci(),
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    }
