import pytest
from habit import Habit
from datetime import datetime, timezone
import pytest  # Add this line at the very top
from habit import Habit

def test_habit_initialization():
    habit = Habit("Test", "daily")
    assert habit.task == "Test"
    assert isinstance(habit.creation_date, datetime)
    assert habit.creation_date.tzinfo == timezone.utc

def test_habit_completion():
    habit = Habit("Test", "weekly")
    completion_time = habit.complete()
    assert isinstance(completion_time, datetime)
    assert completion_time.tzinfo == timezone.utc