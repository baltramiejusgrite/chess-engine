import chess
import chess.engine
from app.search import choose_move

STOCKFISH_PATH = "engines/stockfish.exe"


def play_game(stockfish, my_engine_is_white, skill_level):
    """Play one game: your engine vs Stockfish at a given skill level.
    Returns '1-0', '0-1', or '1/2-1/2'."""
    board = chess.Board()
    stockfish.configure({"Skill Level": skill_level})

    while not board.is_game_over():
        my_turn = (board.turn == chess.WHITE) == my_engine_is_white
        if my_turn:
            move = choose_move(board, depth=4)  # depth 4 keeps benchmark games fast
        else:
            result = stockfish.play(board, chess.engine.Limit(time=0.1))
            move = result.move
        board.push(move)

    return board.result()


def run_benchmark(skill_level, num_games=6):
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    my_wins = my_losses = draws = 0
    for i in range(num_games):
        my_engine_is_white = (i % 2 == 0)  # alternate colors for fairness
        result = play_game(engine, my_engine_is_white, skill_level)

        if result == "1/2-1/2":
            draws += 1
            outcome = "draw"
        else:
            white_won = (result == "1-0")
            my_engine_won = (white_won == my_engine_is_white)
            if my_engine_won:
                my_wins += 1
                outcome = "WIN"
            else:
                my_losses += 1
                outcome = "loss"
        print(f"Game {i+1} (my engine as {'White' if my_engine_is_white else 'Black'}): {outcome}")

    engine.quit()
    print(f"\nvs Stockfish Skill {skill_level}: "
          f"{my_wins} wins, {my_losses} losses, {draws} draws (of {num_games})")


if __name__ == "__main__":
    run_benchmark(skill_level=1, num_games=6)