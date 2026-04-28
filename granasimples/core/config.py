import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DB_PATH = Path(os.getenv("GRANASIMPLES_DB_PATH", DATA_DIR / "granasimples.db"))
