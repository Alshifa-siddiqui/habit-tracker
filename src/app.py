import sys
import os

# Ensure Python recognizes 'src' as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import HabitDatabase
from src.analytics import HabitAnalytics
from src.gui import HabitTrackerGUI
import tkinter as tk


def main():
    db = HabitDatabase()
    analytics = HabitAnalytics()

    while True:
        print("\n📌 Habit Tracker - Menu")
        print("1️⃣ Add a new habit")
        print("2️⃣ Show all habits")
        print("3️⃣ Mark habit as completed")
        print("4️⃣ Show analytics")
        print("5️⃣ Launch GUI")
        print("6️⃣ Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter habit name: ")
            frequency = input("Enter frequency (daily/weekly): ")
            db.add_habit(name, frequency)
            print(f"✅ Habit '{name}' added successfully!")

        elif choice == "2":
            habits = db.get_habits()
            if habits:
                print("\n📋 Tracked Habits:")
                for habit in habits:
                    print(f"{habit[0]} - {habit[1]} ({habit[2]})")
            else:
                print("❌ No habits found.")

        elif choice == "3":
            habit_id = input("Enter habit ID to mark as completed: ")
            if habit_id.isdigit():
                db.check_habit(int(habit_id))
                print(f"✅ Habit {habit_id} marked as completed!")
            else:
                print("⚠️ Please enter a valid habit ID.")

        elif choice == "4":
            report = analytics.generate_report()
            print("\n📊 Habit Statistics:")
            print(report)

        elif choice == "5":
            print("🖥️ Launching GUI...")
            root = tk.Tk()
            app = HabitTrackerGUI(root)
            root.mainloop()

        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            sys.exit()

        else:
            print("⚠️ Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
