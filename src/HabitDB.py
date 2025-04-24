import sqlite3
from datetime import datetime, date
from habit import Habit
from Dates_Persistence import delete_dates, create_file

# ✅ Register adapter/converter for date handling (Python 3.12+ fix)
sqlite3.register_adapter(date, lambda d: d.isoformat())
sqlite3.register_converter("DATE", lambda s: date.fromisoformat(s.decode("utf-8")))

connection = sqlite3.connect("habitDB.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY,
        period TEXT CHECK (period IN ('daily', 'weekly')),
        description TEXT,
        streak INTEGER,
        created_at DATE,
        status TEXT CHECK (status IN ('completed', 'incomplete')),
        broken_count INTEGER,
        duration INTEGER,
        day_week TEXT)
""")
connection.commit()

class HabitDB:
    def __init__(self):
        self.connection = sqlite3.connect("habitDB.db", detect_types=sqlite3.PARSE_DECLTYPES)
        self.habit = Habit(name='zaid', period='daily', description='testing', streak=0,
                           broken_count=0, status='incomplete', created_at=datetime.now().date(),
                           duration=100, day_week="day")

    def habit_exists(self, name):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM habits WHERE name = ?", (name,))
            return cursor.fetchone() is not None

    def create_habit(self, name, period, description, duration, day_week,
                     created_at=datetime.now().date(), streak=0, broken_count=0, status='incomplete'):
        if not name or not period or not description or not duration or not day_week:
            raise ValueError("All required fields must be provided.")
        if period not in ('daily', 'weekly') or day_week not in ('day', 'week'):
            raise ValueError("Invalid period or day/week value")
        if self.habit_exists(name):
            raise ValueError("Habit already exists")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO habits(name, period, description, streak, created_at, status, broken_count, duration, day_week)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, period, description, streak, created_at, status, broken_count, duration, day_week))
            connection.commit()
            create_file(name)

    def delete_habit(self, name):
        if not name:
            raise ValueError("Name not provided")
        if not self.habit_exists(name):
            raise ValueError("Habit not found")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM habits WHERE name = ?", (name,))
            connection.commit()
            delete_dates(name)

    def get_completed_habits(self):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM habits WHERE status = ?", ("completed",))
            return [row[0] for row in cursor.fetchall()]

    def get_incomplete_habits(self):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM habits WHERE status = ?", ("incomplete",))
            return [row[0] for row in cursor.fetchall()]

    def get_streak(self, name):
        if not name or not self.habit_exists(name):
            raise ValueError("Invalid habit name")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT streak FROM habits WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_broken_count(self, name):
        if not name or not self.habit_exists(name):
            raise ValueError("Invalid habit name")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT broken_count FROM habits WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def longest_streak(self):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(streak) FROM habits WHERE status = 'incomplete'")
            return cursor.fetchone()[0]

    def get_description(self, name):
        if not name or not self.habit_exists(name):
            raise ValueError("Invalid habit name")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT description FROM habits WHERE name = ?", (name,))
            return cursor.fetchone()[0]

    def get_period(self, name):
        if not name or not self.habit_exists(name):
            raise ValueError("Invalid habit name")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT period FROM habits WHERE name = ?", (name,))
            return cursor.fetchone()[0]

    def get_habits(self):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM habits")
            return cursor.fetchall()

    def delete_all_habits(self):
        with self.connection as connection:
            cursor = connection.cursor()
            for habit in [h[0] for h in self.get_habits()]:
                delete_dates(habit)
            cursor.execute("DELETE FROM habits")
            connection.commit()

    def update_description(self, name, new_desc):
        if not name or not new_desc or not self.habit_exists(name):
            raise ValueError("Invalid input")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE habits SET description = ? WHERE name = ?", (new_desc, name))
            connection.commit()

    def update_period(self, name, duration, day_week):
        if not name or not duration or not day_week or not self.habit_exists(name):
            raise ValueError("Invalid input")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT period FROM habits WHERE name = ?", (name,))
            period = cursor.fetchone()[0]
            new_period = 'weekly' if period == 'daily' else 'daily'
            cursor.execute("UPDATE habits SET period = ?, duration = ?, day_week = ? WHERE name = ?",
                           (new_period, duration, day_week, name))
            connection.commit()

    def update_status_streak(self, name):
        if not name or not self.habit_exists(name):
            raise ValueError("Invalid habit name")
        curr_streak, broken_count = self.habit.streak_calculations(name)
        with self.connection as connection:
            cursor = connection.cursor()
            duration = self.get_duration(name)
            if curr_streak < duration:
                cursor.execute("UPDATE habits SET streak = ? WHERE name = ?", (curr_streak, name))
            elif curr_streak >= duration:
                cursor.execute("UPDATE habits SET status = 'completed', streak = ? WHERE name = ?", (duration, name))
            if broken_count > self.get_broken_count(name):
                cursor.execute("UPDATE habits SET streak = 0, broken_count = ? WHERE name = ?", (broken_count, name))
            connection.commit()

    def get_duration(self, name):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT duration FROM habits WHERE name = ?", (name,))
            return cursor.fetchone()[0]
