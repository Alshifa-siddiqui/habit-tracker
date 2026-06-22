"""Tests for HabitAnalytics, using a shared in-memory database."""
import pytest

from database import HabitDatabase
from analytics import HabitAnalytics


@pytest.fixture
def setup():
    db = HabitDatabase(":memory:")
    analytics = HabitAnalytics(db)
    yield db, analytics
    db.conn.close()


def test_analytics_shares_injected_connection(setup):
    db, analytics = setup
    assert analytics.db is db  # no second connection opened


def test_completion_rate_weekly(setup):
    db, analytics = setup
    hid = db.add_habit("Run", "daily")
    db.check_habit(hid)
    assert analytics.get_completion_rate(hid, "weekly") == round(1 / 7 * 100, 1)


def test_generate_report_lists_habits(setup):
    db, analytics = setup
    db.add_habit("Read", "daily")
    assert "Read" in analytics.generate_report(1)


def test_compare_habits(setup):
    db, analytics = setup
    h1 = db.add_habit("A", "daily")
    h2 = db.add_habit("B", "daily")
    db.check_habit(h1)
    data = analytics.compare_habits(h1, h2)
    assert set(data.keys()) == {"A", "B"}
    assert data["A"]["check_ins"] == 1


def test_best_day_no_data(setup):
    db, analytics = setup
    hid = db.add_habit("X", "daily")
    assert analytics.get_best_day_of_week(hid) == "No data"
