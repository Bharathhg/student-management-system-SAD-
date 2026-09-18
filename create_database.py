import sqlite3

def init_db():
    conn = sqlite3.connect("students.db")
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
    print("Database Initialized Successfully.")

if __name__ == "__main__":
    init_db()
