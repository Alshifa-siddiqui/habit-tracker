"""Seed the database with the documented sample habits.

Run from the repository root:

    python -m src.seed

Creates the schema if needed and inserts the sample habits, skipping any that
already exist, so it is safe to re-run. The database file itself is not tracked
in git (see .gitignore) — run this once after cloning to load the sample data.
"""
from src.db import connect_db, create_table

SAMPLE_HABITS = [
    ("Drink Water", "Daily", 30),
    ("Gym", "Weekly", 4),
    ("Morning Walk", "Daily", 20),
    ("Yoga", "Weekly", 5),
    ("Journal Writing", "Daily", 25),
]


def seed() -> None:
    create_table()
    conn = connect_db()
    c = conn.cursor()
    added = 0
    for name, periodicity, streak in SAMPLE_HABITS:
        c.execute("SELECT 1 FROM habits WHERE name = ?", (name,))
        if c.fetchone() is None:
            c.execute(
                "INSERT INTO habits (name, periodicity, streak) VALUES (?, ?, ?)",
                (name, periodicity, streak),
            )
            added += 1
    conn.commit()
    conn.close()
    print(f"Seeded {added} new sample habit(s) ({len(SAMPLE_HABITS)} total).")


if __name__ == "__main__":
    seed()
