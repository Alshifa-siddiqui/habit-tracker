import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'habits.db')

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_completed TIMESTAMP,
            streak INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def complete_habit(name):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT streak FROM habits WHERE name = ?', (name,))
    row = c.fetchone()
    if row:
        new_streak = row[0] + 1
        c.execute('UPDATE habits SET last_completed = ?, streak = ? WHERE name = ?', (datetime.now(), new_streak, name))
        conn.commit()
        print(f"Habit '{name}' marked as completed. Current streak: {new_streak}")
    else:
        print("Habit not found.")
    conn.close()

def delete_habit(name):
    conn = connect_db()
    c = conn.cursor()
    c.execute('DELETE FROM habits WHERE name = ?', (name,))
    conn.commit()
    conn.close()
