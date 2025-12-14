import sqlite3
from pathlib import Path

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))
