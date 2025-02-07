import sqlite3

class HabitDatabase:
    def __init__(self, db_name="habits.db"):
        """Initialize database connection."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def add_habit(self, name, frequency):
        """Add a new habit."""
        self.cursor.execute("INSERT INTO habits (name, frequency) VALUES (?, ?)", (name, frequency))
        self.conn.commit()

    def delete_habit(self, habit_id):
        """Delete a habit by ID."""
        self.cursor.execute("DELETE FROM habits WHERE id=?", (habit_id,))
        self.conn.commit()

    def get_habits(self):
        """Retrieve all habits."""
        self.cursor.execute("SELECT * FROM habits")
        return self.cursor.fetchall()

    def check_habit(self, habit_id):
        """Mark a habit as completed."""
        self.cursor.execute("INSERT INTO habit_tracking (habit_id) VALUES (?)", (habit_id,))
        self.conn.commit()

    def get_habit_history(self, habit_id):
        """Get tracking history of a habit."""
        self.cursor.execute("SELECT * FROM habit_tracking WHERE habit_id=?", (habit_id,))
        return self.cursor.fetchall()

    def close(self):
        """Close database connection."""
        self.conn.close()
