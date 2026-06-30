# Chess Engine

A chess engine built using in Python, paired with a web interface and Stockfish integration for higher difficulty tiers. The engine uses minimax search with alpha-beta pruning and a hand-written evaluation function. Players can choose between the custom engine at several depths or Stockfish across a range of strengths.

**Live demo:** [baltramiejus.dev/chess-engine](https://baltramiejus.dev/chess-engine)

## Features

- **Custom chess engine** — minimax search with alpha-beta pruning, move ordering, and a material + positional evaluation function.
- **Six difficulty tiers** — three levels powered by the custom engine (at increasing search depth) and three powered by Stockfish, ranging from beginner to full strength.
- **Play as White, Black, or random** — with board orientation and engine-moves-first handled automatically.
- **Interactive web UI** — drag-to-move, legal-move highlighting, check indication, move/capture/check sound effects, and a clean side panel for game setup.
- **Stockfish integration** — used for the higher difficulty tiers and as a benchmark opponent for measuring the custom engine's strength.

## How the engine works

The engine evaluates positions and searches ahead to choose moves:

**Evaluation function** (`app/evaluation.py`) — scores any position from a single number: positive favors White, negative favors Black. It combines material balance (standard piece values in centipawns) with piece-square tables that reward good placement (e.g. centralized knights, advanced pawns). Checkmate and draw states are scored at the extremes so the search treats them as decisive outcomes.

**Search** (`app/search.py`) — minimax with alpha-beta pruning. The engine looks several moves ahead, assuming both sides play their best, and picks the move with the best guaranteed outcome. Alpha-beta pruning skips branches that cannot affect the result, which dramatically reduces the number of positions searched and makes deeper search practical. Move ordering (trying captures of valuable pieces first) further improves pruning efficiency.

**Strength** — the custom engine was benchmarked against Stockfish at varying skill levels by playing batches of games with alternating colors. At its standard search depth it performs at approximately 1100–1300 Elo — beatable but capable of real, principled play. The higher difficulty tiers delegate to Stockfish, which covers the 2000+ range that a hand-written minimax engine realistically cannot reach.

## Tech stack

- **Backend:** Python, FastAPI, [python-chess](https://python-chess.readthedocs.io/) (move generation and rules)
- **Engine:** Custom minimax + alpha-beta implementation; Stockfish for higher tiers
- **Frontend:** Vanilla JavaScript with chessboard.js and chess.js
- **Deployment:** Docker, Render (Stockfish installed as a system binary in the container)

## Architecture

The FastAPI backend serves the web UI and exposes a `/move` endpoint. The browser tracks the game state (via chess.js) and sends the current position plus the chosen difficulty to the backend, which routes to either the custom engine at a given depth or Stockfish at a given skill level, then returns the chosen move. A cross-platform helper locates the Stockfish binary whether running locally or in the deployed Linux container.

```
app/
├── main.py             # FastAPI app, /move endpoint, difficulty routing
├── search.py           # Minimax + alpha-beta search, move ordering
├── evaluation.py       # Position evaluation (material + piece-square tables)
├── engines_config.py   # Cross-platform Stockfish binary location
├── benchmark.py        # Engine vs Stockfish Elo benchmarking
└── static/             # Web UI (HTML, JS, sounds, images)
```

## Running locally

Requires Python 3.12+ and (optionally) a local Stockfish binary for the Stockfish difficulty tiers.

```bash
# Clone and enter the project
git clone https://github.com/baltramiejusgrite/chess-engine.git
cd chess-engine

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) place a Stockfish binary at engines/stockfish.exe (Windows)
# or install Stockfish system-wide (Linux/Mac) for the Stockfish tiers

# Run the server
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000` in your browser.

## Deployment

The app deploys via Docker. The Dockerfile installs Stockfish as a system package so the engine can find it at runtime, installs the Python dependencies, and runs the FastAPI app with uvicorn. It is currently deployed on Render's free tier.
