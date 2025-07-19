from src.habit import Habit
from src.db import connect_db, create_table, delete_habit, complete_habit

def test_create_habit():
    habit = Habit('Exercise', 'Daily')
    assert habit.name == 'Exercise'
    assert habit.periodicity == 'Daily'

def test_complete_and_delete_habit():
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO habits (name, periodicity) VALUES (?, ?)', ('Read Book', 'Daily'))
    conn.commit()

    complete_habit('Read Book')

    c.execute('SELECT streak FROM habits WHERE name = ?', ('Read Book',))
    row = c.fetchone()
    assert row is not None
    assert row[0] >= 1  # Streak must increase after completion

    delete_habit('Read Book')

    c.execute('SELECT * FROM habits WHERE name = ?', ('Read Book',))
    assert c.fetchone() is None
    conn.close()
