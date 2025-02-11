import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter
from database import HabitDatabase

class HabitAnalytics:
    def __init__(self):
        """Initialize database connection."""
        self.db = HabitDatabase()

    def get_longest_streak(self, habit_id):
        """Find the longest streak of a habit."""
        history = self.db.get_habit_history(habit_id)
        if not history:
            return 0

        dates = sorted([datetime.strptime(entry[2], "%Y-%m-%d %H:%M:%S") for entry in history])
        streaks = []
        streak = 1

        for i in range(len(dates) - 1):
            if (dates[i + 1] - dates[i]).days in [1, 7]:  # Daily or Weekly streak
                streak += 1
            else:
                streaks.append(streak)
                streak = 1
        streaks.append(streak)

        return max(streaks)

    def get_most_consistent_habits(self, top_n=3):
        """Find the top N most consistent habits."""
        habits = self.db.get_habits()
        if not habits:
            return None

        habit_counts = {habit[0]: len(self.db.get_habit_history(habit[0])) for habit in habits}
        sorted_habits = sorted(habit_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_habits[:top_n]

    def get_habits_needing_improvement(self, bottom_n=3):
        """Find the bottom N least completed habits."""
        habits = self.db.get_habits()
        if not habits:
            return None

        habit_counts = {habit[0]: len(self.db.get_habit_history(habit[0])) for habit in habits}
        sorted_habits = sorted(habit_counts.items(), key=lambda x: x[1])
        return sorted_habits[:bottom_n]

    def plot_habit_progress(self, habit_id):
        """Generate a progress graph for a habit."""
        history = self.db.get_habit_history(habit_id)
        if not history:
            print("No data available for this habit.")
            return

        dates = [datetime.strptime(entry[2], "%Y-%m-%d %H:%M:%S") for entry in history]
        count_per_day = Counter([date.date() for date in dates])

        plt.figure(figsize=(10, 5))
        plt.bar(count_per_day.keys(), count_per_day.values(), color="blue")
        plt.xlabel("Date")
        plt.ylabel("Check-ins")
        plt.title("Habit Tracking Progress")
        plt.xticks(rotation=45)
        plt.show()

    def generate_report(self):
        """Generate a textual summary report of habit progress."""
        habits = self.db.get_habits()
        if not habits:
            return "No habits found."

        report = "📊 Habit Tracker Report\n\n"
        for habit in habits:
            if len(habit) == 4:
                habit_id, name, frequency, _ = habit
            elif len(habit) == 3:  # If there's no fourth value
                habit_id, name, frequency = habit
                _ = None  # Assign a default value

            longest_streak = self.get_longest_streak(habit_id)
            check_ins = len(self.db.get_habit_history(habit_id))

            report += f"🔹 Habit: {name}\n"
            report += f"   - Frequency: {frequency}\n"
            report += f"   - Check-ins: {check_ins}\n"
            report += f"   - Longest Streak: {longest_streak} days\n\n"

        return report
