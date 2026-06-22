"""Unit tests for the Vitalis database layer (uses an in-memory SQLite DB)."""
import sqlite3
from datetime import date, timedelta

import pytest

from database import HabitDatabase


@pytest.fixture
def db():
    database = HabitDatabase(":memory:")
    yield database
    database.conn.close()


def test_add_and_get_habit_returns_dicts(db):
    db.add_habit("Exercise", "daily")
    habits = db.get_habits()
    assert len(habits) == 1
    assert habits[0]["name"] == "Exercise"
    assert habits[0]["frequency"] == "daily"


def test_check_habit_returns_xp_and_badges(db):
    hid = db.add_habit("Drink Water", "daily")
    result = db.check_habit(hid)
    assert isinstance(result, tuple)
    xp, new_badges = result
    assert isinstance(xp, int) and xp > 0
    assert "🔥 First Flame" in new_badges  # first check-in badge


def test_check_habit_blocks_second_checkin_same_day(db):
    hid = db.add_habit("Meditation", "daily")
    db.check_habit(hid)
    with pytest.raises(Exception):
        db.check_habit(hid)


def test_streak_continues_when_within_gap(db):
    hid = db.add_habit("Reading", "daily")
    # Simulate a check-in yesterday with a streak of 5.
    yesterday = date.today() - timedelta(days=1)
    db.update_habit(hid, last_completed=yesterday.isoformat(), current_streak=5)
    db.check_habit(hid)
    assert db.get_habit_by_id(hid)["current_streak"] == 6


def test_streak_resets_after_missed_day(db):
    hid = db.add_habit("Walking", "daily")
    # Last check-in was 3 days ago — the daily streak should reset.
    long_ago = date.today() - timedelta(days=3)
    db.update_habit(hid, last_completed=long_ago.isoformat(), current_streak=9)
    db.check_habit(hid)
    assert db.get_habit_by_id(hid)["current_streak"] == 1


def test_weekly_streak_allows_seven_day_gap(db):
    hid = db.add_habit("Weekly Review", "weekly")
    week_ago = date.today() - timedelta(days=7)
    db.update_habit(hid, last_completed=week_ago.isoformat(), current_streak=2)
    db.check_habit(hid)
    assert db.get_habit_by_id(hid)["current_streak"] == 3


def test_update_habit_changes_fields(db):
    hid = db.add_habit("Old Name", "daily")
    db.update_habit(hid, name="New Name", frequency="weekly")
    h = db.get_habit_by_id(hid)
    assert h["name"] == "New Name"
    assert h["frequency"] == "weekly"


def test_delete_habit_by_id(db):
    hid = db.add_habit("Temp", "daily")
    db.delete_habit(hid)
    assert db.get_habit_by_id(hid) is None


def test_delete_habit_cascades_history(db):
    hid = db.add_habit("Temp", "daily")
    db.check_habit(hid)
    assert db.get_habit_history(hid)  # has a check-in
    db.delete_habit(hid)
    assert db.get_habit_history(hid) == []  # no orphaned rows


def test_duplicate_checkin_blocked_at_db_level(db):
    hid = db.add_habit("Temp", "daily")
    today = date.today()
    db.cursor.execute(
        "INSERT INTO habit_history (habit_id, completed_date) VALUES (?, ?)",
        (hid, today))
    with pytest.raises(sqlite3.IntegrityError):
        db.cursor.execute(
            "INSERT INTO habit_history (habit_id, completed_date) VALUES (?, ?)",
            (hid, today))


def test_longest_streak_tracks_best(db):
    hid = db.add_habit("Pushups", "daily")
    yesterday = date.today() - timedelta(days=1)
    db.update_habit(hid, last_completed=yesterday.isoformat(),
                    current_streak=10, longest_streak=10)
    db.check_habit(hid)
    assert db.get_habit_by_id(hid)["longest_streak"] == 11
