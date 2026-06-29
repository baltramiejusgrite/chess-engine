import chess
import time
from app.search import choose_move

board = chess.Board()
start = time.time()
move = choose_move(board, depth=5)
print(f"Engine chose: {move.uci()} in {time.time() - start:.2f}s")