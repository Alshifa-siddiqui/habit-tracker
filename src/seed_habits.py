from habitDB import HabitDB
from habit import Habit
import datetime

def seed():
    db = HabitDB()
    predefined_habits = [
        ("Exercise", "Daily workout for 30 minutes", "daily", 7),
        ("Read Quran", "Read 1 page daily", "daily", 30),
        ("Weekly Review", "Reflect on weekly goals", "weekly", 4),
        ("Clean Room", "Tidy up living space", "weekly", 4),
        ("Stretch", "Morning stretching routine", "daily", 10)
    ]

    for name, desc, period, duration in predefined_habits:
        try:
            db.create_habit(name, desc, period, duration)
            habit = Habit()
            today = datetime.date.today()
            dates = []
            for i in range(4):
                if period == "daily":
                    dates.append(today - datetime.timedelta(days=i))
                elif period == "weekly":
                    dates.append(today - datetime.timedelta(weeks=i))
            for date in dates:
                habit.habit_is_done_on_date(name, date.strftime('%Y-%m-%d'))
        except Exception as e:
            print(f"{name} already exists or failed to insert: {e}")

if __name__ == "__main__":
    seed()
