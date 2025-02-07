import unittest
from src.habit import Habit

class TestHabit(unittest.TestCase):
    def test_create_habit(self):
        habit = Habit(name="Exercise", frequency="Daily")
        self.assertEqual(habit.name, "Exercise")
        self.assertEqual(habit.frequency, "Daily")

if __name__ == "__main__":
    unittest.main()
