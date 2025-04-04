import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_db, create_habit, add_completion, initialize_db
from datetime import datetime, timedelta, timezone

def load_test_data():
    initialize_db()  # 💾 Ensure tables exist

    habits = [
        ("Drink water", "daily"),
        ("Exercise", "daily"),
        ("Read 10 pages", "daily"),
        ("Weekly review", "weekly"),
        ("Family dinner", "weekly")
    ]

    with get_db() as conn:
        conn.execute("DELETE FROM habits")
        conn.execute("DELETE FROM completions")

        for task, periodicity in habits:
            create_habit(conn, task, periodicity)

        # Add completions
        start_date = datetime.now(timezone.utc) - timedelta(weeks=4)
        for day in range(28):
            current_date = start_date + timedelta(days=day)
            for habit_id in [1, 2, 3]:
                add_completion(conn, habit_id)
            if day % 7 == 0:
                for habit_id in [4, 5]:
                    add_completion(conn, habit_id)

if __name__ == "__main__":
    load_test_data()
