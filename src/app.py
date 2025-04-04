import sys
import tkinter as tk
from datetime import datetime, timezone
from src.database import get_db, create_habit, add_completion, delete_habit, initialize_db
from src.analytics import get_all_habits, get_habits_by_periodicity, get_longest_streak
from src.gui import HabitTrackerGUI

def cli_menu():
    """Command-line interface menu"""
    initialize_db()
    
    while True:
        print("\n📌 Habit Tracker - Menu")
        print("1️⃣ Add new habit")
        print("2️⃣ List all habits")
        print("3️⃣ Mark habit as completed")
        print("4️⃣ Show analytics")
        print("5️⃣ Launch GUI")
        print("6️⃣ Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter habit name: ")
            frequency = input("Enter frequency (daily/weekly): ").lower()
            try:
                with get_db() as conn:
                    create_habit(conn, name, frequency)
                print(f"✅ Habit '{name}' added successfully!")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        elif choice == "2":
            with get_db() as conn:
                habits = get_all_habits(conn)
                if habits:
                    print("\n📋 Tracked Habits:")
                    for habit in habits:
                        print(f"ID: {habit['id']} | {habit['task']} ({habit['periodicity']})")
                else:
                    print("❌ No habits found.")

        elif choice == "3":
            habit_id = input("Enter habit ID to mark as completed: ")
            if habit_id.isdigit():
                try:
                    with get_db() as conn:
                        add_completion(conn, int(habit_id))
                    print(f"✅ Habit {habit_id} marked as completed!")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
            else:
                print("⚠️ Please enter a valid habit ID.")

        elif choice == "4":
            with get_db() as conn:
                print("\n📊 Habit Analytics:")
                print(f"Longest Overall Streak: {get_longest_streak(conn)} days")
                
                print("\nDaily Habits:")
                for habit in get_habits_by_periodicity(conn, "daily"):
                    streak = get_longest_streak(conn, habit['id'])
                    print(f"- {habit['task']}: {streak} day streak")
                
                print("\nWeekly Habits:")
                for habit in get_habits_by_periodicity(conn, "weekly"):
                    streak = get_longest_streak(conn, habit['id'])
                    print(f"- {habit['task']}: {streak} week streak")

        elif choice == "5":
            print("🖥️ Launching GUI...")
            root = tk.Tk()
            app = HabitTrackerGUI(root)
            root.mainloop()

        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            sys.exit()

        else:
            print("⚠️ Invalid choice! Please select 1-6.")

if __name__ == "__main__":
    cli_menu()