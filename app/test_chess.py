import chess

# Create a fresh board (standard starting position)
board = chess.Board()
print(board)
print()

# How many legal moves does White have at the start?
legal_moves = list(board.legal_moves)
print("Number of legal moves:", len(legal_moves))
print("First few:", legal_moves[:5])

# Make a move (e2 to e4) and show the board
board.push(chess.Move.from_uci("e2e4"))
print()
print(board)

# Useful checks the engine will rely on later
print()
print("Is it checkmate?", board.is_checkmate())
print("Is the game over?", board.is_game_over())
print("Whose turn?", "White" if board.turn else "Black")