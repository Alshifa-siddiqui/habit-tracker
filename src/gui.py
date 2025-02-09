import sys
import os
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from database import HabitDatabase
from src.analytics import HabitAnalytics

class HabitTrackerGUI:
    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.db = HabitDatabase()
        self.analytics = HabitAnalytics()

        # UI Elements
        tk.Label(root, text="Habit Name:").grid(row=0, column=0, padx=10, pady=5)
        self.habit_entry = tk.Entry(root)
        self.habit_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Frequency (Daily/Weekly):").grid(row=1, column=0, padx=10, pady=5)
        self.frequency_entry = tk.Entry(root)
        self.frequency_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(root, text="Add Habit", command=self.add_habit, bg="green", fg="white").grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Show Habits", command=self.show_habits, bg="blue", fg="white").grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Mark Habit Complete", command=self.mark_habit_complete, bg="orange", fg="white").grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Show Statistics", command=self.show_statistics, bg="purple", fg="white").grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").grid(row=6, column=0, columnspan=2, pady=5)

    def add_habit(self):
        """Add a new habit to the database."""
        name = self.habit_entry.get().strip()
        frequency = self.frequency_entry.get().strip()
        if name and frequency:
            self.db.add_habit(name, frequency)
            messagebox.showinfo("Success", f"Habit '{name}' added!")
            self.habit_entry.delete(0, tk.END)
            self.frequency_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter both habit name and frequency.")

    def show_habits(self):
        """Display all active habits."""
        habits = self.db.get_active_habits()
        habit_list = "\n".join([f"ID: {habit[0]} - {habit[1]} ({habit[2]})" for habit in habits])
        messagebox.showinfo("Tracked Habits", habit_list if habit_list else "No active habits found.")

    def mark_habit_complete(self):
        """Mark a habit as completed and update streaks."""
        habit_id = self.habit_entry.get().strip()
        if habit_id.isdigit():
            habit_id = int(habit_id)
            self.db.check_habit(habit_id)
            messagebox.showinfo("Success", f"Habit {habit_id} marked as completed!")

            # Refresh the habit list after marking complete
            self.show_habits()
        else:
            messagebox.showwarning("Warning", "Please enter a valid habit ID.")

    def show_statistics(self):
        """Show analytics and statistics for habits."""
        habits = self.db.get_habits()
        stats = "\n".join([f"ID: {habit[0]} - {habit[1]} | Streak: {self.db.get_streak(habit[0])} days" for habit in habits])
        messagebox.showinfo("Habit Statistics", stats if stats else "No habits found.")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
