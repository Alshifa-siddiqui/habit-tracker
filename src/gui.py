import sys
import os
import tkinter as tk
from tkinter import messagebox
from src.database import HabitDatabase
from src.analytics import HabitAnalytics

# Ensure Python recognizes 'src' as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class HabitTrackerGUI:
    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x300")  # Set window size
        self.root.configure(bg="#f7f7f7")  # Background color

        self.db = HabitDatabase()
        self.analytics = HabitAnalytics()

        # UI Elements
        frame = tk.Frame(root, padx=20, pady=20, bg="#f7f7f7")
        frame.pack(expand=True)

        tk.Label(frame, text="Habit Name:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, sticky="w", pady=5)
        self.habit_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.habit_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Frequency (Daily/Weekly):", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, sticky="w", pady=5)
        self.frequency_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.frequency_entry.grid(row=1, column=1, pady=5)

        # Buttons
        btn_style = {"font": ("Arial", 12), "width": 20, "bg": "#4CAF50", "fg": "white"}

        self.add_button = tk.Button(frame, text="Add Habit", command=self.add_habit, **btn_style)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.list_button = tk.Button(frame, text="Show Habits", command=self.show_habits, **btn_style)
        self.list_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.check_button = tk.Button(frame, text="Mark Habit Complete", command=self.mark_habit_complete, **btn_style)
        self.check_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.stats_button = tk.Button(frame, text="Show Statistics", command=self.show_statistics, **btn_style)
        self.stats_button.grid(row=5, column=0, columnspan=2, pady=5)

    def add_habit(self):
        """Add a new habit to the database."""
        name = self.habit_entry.get()
        frequency = self.frequency_entry.get()
        if name and frequency:
            self.db.add_habit(name, frequency)
            messagebox.showinfo("Success", f"Habit '{name}' added!")
        else:
            messagebox.showwarning("Warning", "Please enter both habit name and frequency.")

    def show_habits(self):
        """Display all habits."""
        habits = self.db.get_habits()
        habit_list = "\n".join([f"{habit[0]} - {habit[1]} ({habit[2]})" for habit in habits])
        messagebox.showinfo("Tracked Habits", habit_list if habit_list else "No habits found.")

    def mark_habit_complete(self):
        """Mark a habit as completed."""
        habit_id = self.habit_entry.get()
        if habit_id.isdigit():
            self.db.check_habit(int(habit_id))
            messagebox.showinfo("Success", f"Habit {habit_id} marked as completed!")
        else:
            messagebox.showwarning("Warning", "Please enter a valid habit ID.")

    def show_statistics(self):
        """Show analytics and statistics."""
        report = self.analytics.generate_report()
        messagebox.showinfo("Habit Statistics", report)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
