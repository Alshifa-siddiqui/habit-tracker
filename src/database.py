import sqlite3
import datetime

class HabitDatabase:
    def __init__(self):
        """Connect to the SQLite database and create tables if they don't exist."""
        self.conn = sqlite3.connect("habits.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables for habits and check-ins."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        """)
        self.conn.commit()

    def delete_habit(self, habit_id):
         """Delete a habit from the database along with its check-in history."""
         self.cursor.execute("DELETE FROM check_ins WHERE habit_id = ?", (habit_id,))
    self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    self.conn.commit()


    def add_habit(self, name, frequency):
        """Insert a new habit into the database."""
        self.cursor.execute("INSERT INTO habits (name, frequency) VALUES (?, ?)", (name, frequency))
        self.conn.commit()

    def get_habits(self):
        """Retrieve all habits from the database."""
        self.cursor.execute("SELECT id, name, frequency FROM habits")
        return self.cursor.fetchall()

    def check_habit(self, habit_id):
        """Mark a habit as completed by adding a check-in date with timestamp."""
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO habit_checkins (habit_id, date) VALUES (?, ?)", (habit_id, today))
        self.conn.commit()

    def get_habit_history(self, habit_id):
        """Retrieve check-in history for a given habit."""
        self.cursor.execute("SELECT * FROM habit_checkins WHERE habit_id = ?", (habit_id,))
        return self.cursor.fetchall()

    def get_active_habits(self):
        """Retrieve only active habits (habits that have not been completed today)."""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT id, name, frequency FROM habits 
            WHERE id NOT IN (SELECT habit_id FROM habit_checkins WHERE date LIKE ?)
        """, (today + "%",))
        return self.cursor.fetchall()

    def get_streak(self, habit_id):
        """Calculate the streak for a habit based on consecutive check-ins."""
        self.cursor.execute("SELECT date FROM habit_checkins WHERE habit_id = ? ORDER BY date DESC", (habit_id,))
        dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").date() for row in self.cursor.fetchall()]

        if not dates:
            return 0  # No check-ins, no streak

        streak = 1
        for i in range(len(dates) - 1):
            if (dates[i] - dates[i + 1]).days == 1:  # Check if check-ins are consecutive
                streak += 1
            else:
                break  # Streak is broken

        return streak

    def remove_habit(self, habit_id):
        """Remove a habit and its check-ins from the database."""
        self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.cursor.execute("DELETE FROM habit_checkins WHERE habit_id = ?", (habit_id,))
        self.conn.commit()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
