import unittest
from src.database import HabitDatabase

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database before each test."""
        self.db = HabitDatabase(":memory:")  # Use an in-memory DB for testing

    def test_add_habit(self):
        self.db.add_habit("Exercise", "Daily")
        habits = self.db.get_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0][1], "Exercise")  # Check habit name

if __name__ == "__main__":
    unittest.main()
