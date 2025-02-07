from datetime import datetime, timedelta
from src.database import HabitDatabase

class Habit:
    def __init__(self, name, frequency):
        """Initialize a habit with a name and frequency."""
        self.name = name
        self.frequency = frequency
        self.db = HabitDatabase()

    def save(self):
        """Save the habit to the database."""
        self.db.add_habit(self.name, self.frequency)

    def mark_complete(self, habit_id):
        """Mark a habit as completed."""
        self.db.check_habit(habit_id)

    def get_streak(self, habit_id):
        """Calculate current streak of a habit."""
        history = self.db.get_habit_history(habit_id)
        if not history:
            return 0

        dates = sorted([datetime.strptime(entry[2], "%Y-%m-%d %H:%M:%S") for entry in history])
        streak = 1
        for i in range(len(dates) - 1, 0, -1):
            if (dates[i] - dates[i - 1]).days in [1, 7]:  # Daily or Weekly streak
                streak += 1
            else:
                break
        return streak

    def __str__(self):
        """String representation of the habit."""
        return f"Habit(Name: {self.name}, Frequency: {self.frequency})"
