import os
import shutil

def find_stockfish():
    """Locate the Stockfish binary, whether local (Windows) or on Railway (Linux)."""
    system_stockfish = shutil.which("stockfish")
    if system_stockfish:
        return system_stockfish
    local = os.path.join("engines", "stockfish.exe")
    if os.path.exists(local):
        return local
    raise FileNotFoundError("Stockfish binary not found")