import sys
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from database import HabitDatabase

class HabitTrackerGUI:
    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.db = HabitDatabase()

        # UI Elements
        tk.Label(root, text="Habit ID:").grid(row=0, column=0, padx=10, pady=5)
        self.habit_entry = tk.Entry(root)
        self.habit_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(root, text="Check-in Habit", command=self.mark_habit_complete, bg="green", fg="white").grid(row=1, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Show Statistics", command=self.show_statistics, bg="blue", fg="white").grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Weekly Summary", command=self.show_weekly_summary, bg="purple", fg="white").grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").grid(row=4, column=0, columnspan=2, pady=5)

    def mark_habit_complete(self):
        """Mark a habit as completed with a timestamp."""
        habit_id = self.habit_entry.get().strip()
        if habit_id.isdigit():
            habit_id = int(habit_id)
            self.db.check_habit(habit_id)
            messagebox.showinfo("Success", f"Habit {habit_id} checked in successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a valid habit ID.")

    def show_statistics(self):
        """Show check-in logs for each habit."""
        habit_id = self.habit_entry.get().strip()
        if habit_id.isdigit():
            habit_id = int(habit_id)
            check_ins = self.db.get_habit_check_ins(habit_id)
            if check_ins:
                log = "\n".join([f"{date} {time}" for date, time in check_ins])
                messagebox.showinfo("Habit Check-ins", f"Check-ins for Habit {habit_id}:\n{log}")
            else:
                messagebox.showinfo("Habit Check-ins", "No check-ins found for this habit.")
        else:
            messagebox.showwarning("Warning", "Please enter a valid habit ID.")

    def show_weekly_summary(self):
        """Display a weekly summary with a pie chart."""
        summary_data = self.db.get_weekly_summary()
        if summary_data:
            habits, counts = zip(*summary_data)
            plt.figure(figsize=(6, 6))
            plt.pie(counts, labels=habits, autopct="%1.1f%%", colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            plt.title("Weekly Habit Completion Summary")
            plt.show()
        else:
            messagebox.showinfo("Weekly Summary", "No habits tracked this week.")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
