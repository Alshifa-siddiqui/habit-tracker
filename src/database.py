import sqlite3
from datetime import datetime, timezone
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('habits.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def initialize_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            task TEXT UNIQUE,
            periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')),
            creation_date TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS completions (
            habit_id INTEGER,
            completion_date TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )''')

def create_habit(conn, task: str, periodicity: str):
    # Check for duplicates
    cur = conn.execute("SELECT id FROM habits WHERE task = ?", (task,))
    if cur.fetchone():
        raise ValueError("Habit already exists!")
    
    if periodicity not in ['daily', 'weekly']:
        raise ValueError("Invalid periodicity. Use 'daily' or 'weekly'")
    
    conn.execute(
        "INSERT INTO habits (task, periodicity, creation_date) VALUES (?, ?, ?)",
        (task, periodicity, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()

def add_completion(conn, habit_id: int):
    conn.execute(
        "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
        (habit_id, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()

def delete_habit(conn, habit_id: int):
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    conn.commit()