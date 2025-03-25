import sqlite3
from datetime import datetime, timedelta

class HabitDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("habits.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                frequency TEXT,
                day_of_week TEXT DEFAULT NULL,
                date_of_month TEXT DEFAULT NULL,
                completed_count INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                last_completed DATE DEFAULT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add_habit(self, name, frequency, days=None, dates=None):
        try:
            self.cursor.execute(
                "INSERT INTO habits (name, frequency, day_of_week, date_of_month) VALUES (?, ?, ?, ?)",
                (name, frequency, days, dates)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception(f"Habit '{name}' already exists.")

    def update_habit(self, old_name, new_name, new_frequency, days=None, dates=None):
        self.cursor.execute(
            "UPDATE habits SET name=?, frequency=?, day_of_week=?, date_of_month=? WHERE name=?",
            (new_name, new_frequency, days, dates, old_name)
        )
        self.conn.commit()

    def delete_habit(self, name):
        self.cursor.execute("DELETE FROM habits WHERE name=?", (name,))
        self.conn.commit()

    def get_habits(self):
        self.cursor.execute("SELECT * FROM habits")
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_habit_details(self, name):
        self.cursor.execute("SELECT * FROM habits WHERE name=?", (name,))
        row = self.cursor.fetchone()
        if not row:
            return None
        columns = [col[0] for col in self.cursor.description]
        return dict(zip(columns, row))
