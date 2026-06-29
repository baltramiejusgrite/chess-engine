import chess
from app.evaluation import evaluate, PIECE_VALUES


def order_moves(board: chess.Board):
    def move_score(move):
        score = 0
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                score = 10 * PIECE_VALUES[victim.piece_type] - PIECE_VALUES[attacker.piece_type]
        if move.promotion:
            score += PIECE_VALUES[move.promotion]
        return score
    return sorted(board.legal_moves, key=move_score, reverse=True)


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        best = -float("inf")
        for move in order_moves(board):
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float("inf")
        for move in order_moves(board):
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def choose_move(board: chess.Board, depth: int = 5) -> chess.Move:
    maximizing = board.turn == chess.WHITE
    best_move = None
    best_score = -float("inf") if maximizing else float("inf")
    alpha = -float("inf")
    beta = float("inf")

    for move in order_moves(board):
        board.push(move)
        score = minimax(board, depth - 1, alpha, beta, not maximizing)
        board.pop()
        if maximizing and score > best_score:
            best_score, best_move = score, move
            alpha = max(alpha, best_score)
        elif not maximizing and score < best_score:
            best_score, best_move = score, move
            beta = min(beta, best_score)

    return best_move