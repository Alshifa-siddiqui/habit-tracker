import pytest
from database import get_db, create_habit, add_completion, delete_habit
from datetime import datetime, timezone
from freezegun import freeze_time
import pytest  # Add this line at the very top
from database import get_db, create_habit, add_completion, delete_habit

@pytest.fixture
def test_db():
    with get_db() as conn:
        conn.execute("DELETE FROM habits")
        conn.execute("DELETE FROM completions")
        yield conn

def test_habit_creation(test_db):
    create_habit(test_db, "Test habit", "daily")
    row = test_db.execute("SELECT * FROM habits").fetchone()
    assert row['task'] == "Test habit"
    assert row['periodicity'] == "daily"

def test_duplicate_habit(test_db):
    create_habit(test_db, "Dupe test", "weekly")
    with pytest.raises(ValueError):
        create_habit(test_db, "Dupe test", "weekly")

def test_completion_logging(test_db):
    create_habit(test_db, "Test", "daily")
    habit_id = test_db.execute("SELECT last_insert_rowid()").fetchone()[0]
    add_completion(test_db, habit_id)
    completions = test_db.execute("SELECT * FROM completions").fetchall()
    assert len(completions) == 1