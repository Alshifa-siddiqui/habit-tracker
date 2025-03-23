from database import HabitDatabase


class HabitAnalytics:
    def __init__(self):
        """Initialize analytics with the database connection."""
        self.db = HabitDatabase()

    def get_completion_rate(self, habit_id):
        """Dummy function to return random completion rate."""
        return 50  # Placeholder, should be implemented based on real data


if __name__ == "__main__":
    analytics = HabitAnalytics()
