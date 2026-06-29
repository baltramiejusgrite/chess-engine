import chess
from app.evaluation import evaluate

board = chess.Board()
print("Starting position:", evaluate(board))

# A knight developed to the center vs sitting at home
board2 = chess.Board()
board2.push(chess.Move.from_uci("g1f3"))  # knight out toward center
print("After Nf3 (Black to move):", evaluate(board2))