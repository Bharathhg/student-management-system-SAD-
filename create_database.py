import sqlite3
import os

DB_DIR = os.environ.get("DB_DIR", "data")
DB_PATH = os.path.join(DB_DIR, "students.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        usn TEXT NOT NULL,
        dept TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print(f"Database Initialized Successfully at {DB_PATH}.")

if __name__ == "__main__":
    init_db()
