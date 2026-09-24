from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "vehicle_management.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        conn.executescript(file.read())
    return conn
