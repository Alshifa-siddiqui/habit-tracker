"""Unit tests for the habit tracker.

Each test runs against an isolated temporary SQLite database (via a fixture
that repoints the module-level DB_PATH), so tests never mutate the shipped
data/habits.db and don't depend on import order or prior state.
"""
import importlib

import pytest

from src.habit import Habit
from src import db as db_module
from src import analytics as analytics_module


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point db + analytics at a fresh temp database and create the schema."""
    db_file = tmp_path / "test_habits.db"
    monkeypatch.setattr(db_module, "DB_PATH", str(db_file))
    monkeypatch.setattr(analytics_module, "DB_PATH", str(db_file))
    db_module.create_table()
    return str(db_file)


def test_create_habit():
    habit = Habit("Exercise", "Daily")
    assert habit.name == "Exercise"
    assert habit.periodicity == "Daily"


def test_create_table_is_idempotent(temp_db):
    # Calling twice must not raise (CREATE TABLE IF NOT EXISTS).
    db_module.create_table()
    db_module.create_table()


def test_complete_and_delete_habit(temp_db):
    conn = db_module.connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO habits (name, periodicity) VALUES (?, ?)", ("Read Book", "Daily"))
    conn.commit()
    conn.close()

    db_module.complete_habit("Read Book")

    conn = db_module.connect_db()
    c = conn.cursor()
    c.execute("SELECT streak FROM habits WHERE name = ?", ("Read Book",))
    row = c.fetchone()
    assert row is not None
    assert row[0] >= 1  # streak increments after completion

    db_module.delete_habit("Read Book")
    c.execute("SELECT * FROM habits WHERE name = ?", ("Read Book",))
    assert c.fetchone() is None
    conn.close()


def test_analytics_all_and_by_periodicity(temp_db):
    conn = db_module.connect_db()
    conn.execute("INSERT INTO habits (name, periodicity, streak) VALUES ('Water', 'Daily', 30)")
    conn.execute("INSERT INTO habits (name, periodicity, streak) VALUES ('Gym', 'Weekly', 4)")
    conn.commit()
    conn.close()

    assert len(analytics_module.get_all_habits()) == 2
    daily = analytics_module.get_habits_by_periodicity("Daily")
    assert daily == [("Water",)]


def test_longest_streak(temp_db):
    conn = db_module.connect_db()
    conn.execute("INSERT INTO habits (name, periodicity, streak) VALUES ('Water', 'Daily', 30)")
    conn.execute("INSERT INTO habits (name, periodicity, streak) VALUES ('Gym', 'Weekly', 4)")
    conn.commit()
    conn.close()

    name, streak = analytics_module.get_longest_streak()
    assert name == "Water"
    assert streak == 30
