"""Tests for the reminder due-check logic (pure static method on the GUI)."""
from datetime import date

from gui import VitalisApp

TODAY = date.today().isoformat()


def _habit(**over):
    base = {"reminder_time": "08:00", "archived": 0, "last_completed": None}
    base.update(over)
    return base


def test_due_when_time_matches_and_not_done():
    assert VitalisApp._reminder_due(_habit(), "08:00", TODAY) is True


def test_not_due_when_time_differs():
    assert VitalisApp._reminder_due(_habit(), "09:00", TODAY) is False


def test_not_due_without_reminder_time():
    assert VitalisApp._reminder_due(_habit(reminder_time=None), "08:00", TODAY) is False
    assert VitalisApp._reminder_due(_habit(reminder_time=""), "08:00", TODAY) is False


def test_not_due_when_archived():
    assert VitalisApp._reminder_due(_habit(archived=1), "08:00", TODAY) is False


def test_not_due_when_already_completed_today():
    assert VitalisApp._reminder_due(_habit(last_completed=TODAY), "08:00", TODAY) is False
