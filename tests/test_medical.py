"""Unit tests for the medical/wellness pure functions."""
from medical import (MEDICAL_DISCLAIMER, detect_habit_type,
                     get_medical_insight, get_health_score)


def test_disclaimer_present():
    assert "not medical advice" in MEDICAL_DISCLAIMER.lower()


def test_detect_habit_type_matches_keywords():
    assert detect_habit_type("Morning Run") == "exercise"
    assert detect_habit_type("Drink Water") == "water"
    assert detect_habit_type("Quantum Tinkering") is None


def test_get_medical_insight_status_scales_with_rate():
    high = get_medical_insight("Drink Water", 90)
    low = get_medical_insight("Drink Water", 5)
    assert high["status"] == "Excellent"
    assert low["status"] == "Critical"


def test_get_medical_insight_returns_none_for_unknown_habit():
    assert get_medical_insight("Play Chess", 50) is None


def test_health_score_empty_is_na():
    assert get_health_score([])["grade"] == "N/A"
