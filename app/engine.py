import chess
import random


def choose_move(board: chess.Board) -> chess.Move:
    """The 'dumb' engine: pick a random legal move.
    This is our baseline. Later phases replace this with real search."""
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)


def play_game():
    """Play a game in the terminal: you are White, the engine is Black."""
    board = chess.Board()

    while not board.is_game_over():
        print()
        print(board)
        print()

        if board.turn == chess.WHITE:
            # Your turn — type a move in UCI format, e.g. e2e4
            move_str = input("Your move (e.g. e2e4, or 'quit'): ").strip()

            if move_str == "quit":
                print("Game ended.")
                return

            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move, try again.")
            except ValueError:
                print("Invalid format. Use UCI like 'e2e4'.")
        else:
            # Engine's turn
            engine_move = choose_move(board)
            print(f"Engine plays: {engine_move.uci()}")
            board.push(engine_move)

    print()
    print(board)
    print()
    print("Game over:", board.result())


if __name__ == "__main__":
    play_game()