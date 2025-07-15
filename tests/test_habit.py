from src.habit import Habit

def test_create_habit():
    habit = Habit('Exercise', 'Daily')
    assert habit.name == 'Exercise'
    assert habit.periodicity == 'Daily'
