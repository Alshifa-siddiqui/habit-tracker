import sqlite3


class HabitDatabase:
    def __init__(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect("habits.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create habits table if it does not exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_habit(self, name, frequency):
        """Add a new habit to the database."""
        self.cursor.execute("INSERT INTO habits (name, frequency) VALUES (?, ?)", (name, frequency))
        self.conn.commit()

    def get_habits(self):
        """Retrieve all habits from the database."""
        self.cursor.execute("SELECT * FROM habits")
        return self.cursor.fetchall()


if __name__ == "__main__":
    db = HabitDatabase()
