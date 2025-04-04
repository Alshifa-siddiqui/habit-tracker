from datetime import datetime
from typing import List, Dict
import sqlite3

def get_all_habits(conn: sqlite3.Connection) -> List[Dict]:
    return [dict(row) for row in conn.execute("SELECT * FROM habits").fetchall()]

def get_habits_by_periodicity(conn: sqlite3.Connection, periodicity: str) -> List[Dict]:
    return [dict(row) for row in conn.execute(
        "SELECT * FROM habits WHERE periodicity = ?", (periodicity,)
    ).fetchall()]

def get_longest_streak(conn: sqlite3.Connection, habit_id: int = None) -> int:
    query = """
    SELECT completion_date FROM completions
    WHERE habit_id = ? OR ? IS NULL
    ORDER BY completion_date
    """
    params = (habit_id, habit_id) if habit_id else (None, None)
    dates = [datetime.fromisoformat(row[0]) for row in conn.execute(query, params)]
    
    if not dates:
        return 0
    
    periodicity = "daily"
    if habit_id:
        periodicity = conn.execute(
            "SELECT periodicity FROM habits WHERE id = ?", (habit_id,)
        ).fetchone()[0]

    streaks = []
    current_streak = 1
    
    for i in range(1, len(dates)):
        prev = dates[i-1]
        curr = dates[i]
        
        if periodicity == "daily":
            if (curr - prev).days == 1:
                current_streak += 1
            else:
                streaks.append(current_streak)
                current_streak = 1
        else:
            prev_week = prev.isocalendar()[1]
            curr_week = curr.isocalendar()[1]
            if (curr - prev).days >= 7 and curr_week == prev_week + 1:
                current_streak += 1
            else:
                streaks.append(current_streak)
                current_streak = 1
    
    streaks.append(current_streak)
    return max(streaks) if streaks else 0