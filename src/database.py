import sqlite3
import datetime

class HabitDatabase:
    def __init__(self):
        """Connect to the SQLite database and create tables if they don't exist."""
        self.conn = sqlite3.connect("habits.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables for habits and check-ins with timestamps."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS check_ins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                date DATE NOT NULL,
                time TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        """)
        self.conn.commit()

    def add_habit(self, name, frequency):
        """Insert a new habit into the database."""
        self.cursor.execute("INSERT INTO habits (name, frequency) VALUES (?, ?)", (name, frequency))
        self.conn.commit()

    def check_habit(self, habit_id):
        """Mark a habit as completed with timestamp."""
        today = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get the current time
        self.cursor.execute("INSERT INTO check_ins (habit_id, date, time) VALUES (?, ?, ?)", (habit_id, today, current_time))
        self.conn.commit()

    def get_habit_check_ins(self, habit_id):
        """Get all check-ins for a habit (Date & Time)."""
        self.cursor.execute("SELECT date, time FROM check_ins WHERE habit_id = ? ORDER BY date DESC", (habit_id,))
        return self.cursor.fetchall()

    def get_weekly_summary(self):
        """Generate a weekly summary of completed habits."""
        seven_days_ago = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT habits.name, COUNT(check_ins.id) 
            FROM check_ins 
            JOIN habits ON habits.id = check_ins.habit_id 
            WHERE check_ins.date >= ? 
            GROUP BY habits.name
        """, (seven_days_ago,))
        return self.cursor.fetchall()
