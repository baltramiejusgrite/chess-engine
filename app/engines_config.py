import os
import shutil


def find_stockfish():
    """Locate the Stockfish binary across environments.

    Order:
      1. `stockfish` on PATH (works if installed to a PATH dir)
      2. Common Debian/Ubuntu apt install location (/usr/games/stockfish)
      3. Other common Linux locations
      4. Local Windows fallback (engines/stockfish.exe)
    """
    # 1. On PATH
    on_path = shutil.which("stockfish")
    if on_path:
        return on_path

    # 2 & 3. Common Linux install locations (apt installs to /usr/games)
    linux_candidates = [
        "/usr/games/stockfish",
        "/usr/bin/stockfish",
        "/usr/local/bin/stockfish",
    ]
    for path in linux_candidates:
        if os.path.exists(path):
            return path

    # 4. Local Windows fallback
    local = os.path.join("engines", "stockfish.exe")
    if os.path.exists(local):
        return local

    raise FileNotFoundError("Stockfish binary not found")