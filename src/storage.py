import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def get_db_path():
    db_dir = Path(__file__).resolve().parent.parent / "data"
    db_dir.mkdir(exist_ok=True)
    return db_dir / "forecasts.db"
# test.py
from src.storage import get_db_path

db_path = get_db_path()
print(f"Database will be at: {db_path}")