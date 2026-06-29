import chess
import chess.engine

# Path to the Stockfish binary
STOCKFISH_PATH = "engines/stockfish.exe"

# Launch Stockfish
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Ask it for a move from the starting position
board = chess.Board()
result = engine.play(board, chess.engine.Limit(time=0.5))  # think for 0.5 seconds

print("Stockfish chose:", result.move.uci())

engine.quit()  # always close the engine when done