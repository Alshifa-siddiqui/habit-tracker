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


def _seed_history(db, habit_id, days_ago):
    """Insert check-in rows N days before today (derived stats read these)."""
    for n in days_ago:
        d = (date.today() - timedelta(days=n)).isoformat()
        db.cursor.execute(
            "INSERT OR IGNORE INTO habit_history (habit_id, completed_date) VALUES (?, ?)",
            (habit_id, d))
    db.conn.commit()


def test_current_streak_counts_consecutive_days(db):
    hid = db.add_habit("Reading", "daily")
    _seed_history(db, hid, [2, 1, 0])  # three consecutive days incl. today
    assert db.get_habit_by_id(hid)["current_streak"] == 3


def test_current_streak_zero_when_window_lapsed(db):
    hid = db.add_habit("Walking", "daily")
    _seed_history(db, hid, [5, 4, 3])  # 3-day run, but last was 3 days ago
    h = db.get_habit_by_id(hid)
    assert h["current_streak"] == 0    # broken: missed the daily window
    assert h["longest_streak"] == 3    # best run still reported


def test_checkin_extends_streak_from_history(db):
    hid = db.add_habit("Daily", "daily")
    _seed_history(db, hid, [1])        # checked in yesterday
    db.check_habit(hid)               # check in today
    assert db.get_habit_by_id(hid)["current_streak"] == 2


def test_weekly_streak_allows_seven_day_gap(db):
    hid = db.add_habit("Weekly Review", "weekly")
    _seed_history(db, hid, [14, 7, 0])  # once a week incl. today
    assert db.get_habit_by_id(hid)["current_streak"] == 3


def test_completed_count_derived_from_history(db):
    hid = db.add_habit("Counter", "daily")
    _seed_history(db, hid, [3, 2, 1, 0])
    assert db.get_habit_by_id(hid)["completed_count"] == 4


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


def test_longest_streak_tracks_best_run(db):
    hid = db.add_habit("Pushups", "daily")
    _seed_history(db, hid, [10, 9, 8, 5, 0])  # runs of length 3, 1, 1
    assert db.get_habit_by_id(hid)["longest_streak"] == 3


def test_freeze_forgives_missed_day_and_revives_streak(db):
    hid = db.add_habit("Run", "daily")
    _seed_history(db, hid, [3, 2])           # last check-in was 2 days ago
    assert db.get_habit_by_id(hid)["current_streak"] == 0   # broken without a freeze
    db.add_streak_freeze(hid, 1)
    assert db.use_streak_freeze(hid) is True  # forgive yesterday
    h = db.get_habit_by_id(hid)
    assert h["current_streak"] == 2           # streak alive again
    assert h["completed_count"] == 2          # frozen day is NOT a completion
    assert h["streak_freeze"] == 0            # token consumed


def test_use_freeze_fails_without_tokens(db):
    hid = db.add_habit("Run", "daily")
    _seed_history(db, hid, [3, 2])
    assert db.use_streak_freeze(hid) is False  # no tokens to spend


def test_use_freeze_noop_when_not_at_risk(db):
    hid = db.add_habit("Run", "daily")
    _seed_history(db, hid, [1, 0])             # checked in yesterday and today
    db.add_streak_freeze(hid, 1)
    assert db.use_streak_freeze(hid) is False  # nothing to forgive
    assert db.get_habit_by_id(hid)["streak_freeze"] == 1  # token not wasted


def test_delete_habit_cascades_freezes(db):
    hid = db.add_habit("Run", "daily")
    _seed_history(db, hid, [3, 2])
    db.add_streak_freeze(hid, 1)
    db.use_streak_freeze(hid)
    db.delete_habit(hid)
    db.cursor.execute("SELECT COUNT(*) FROM streak_freezes WHERE habit_id=?", (hid,))
    assert db.cursor.fetchone()[0] == 0
