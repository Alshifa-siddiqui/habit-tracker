import tkinter as tk
from tkinter import messagebox
from src.database import HabitDatabase
from src.analytics import HabitAnalytics

class HabitTrackerGUI:
    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.db = HabitDatabase()
        self.analytics = HabitAnalytics()

        # UI Elements
        self.habit_label = tk.Label(root, text="Habit Name:")
        self.habit_label.pack()

        self.habit_entry = tk.Entry(root)
        self.habit_entry.pack()

        self.frequency_label = tk.Label(root, text="Frequency (Daily/Weekly):")
        self.frequency_label.pack()

        self.frequency_entry = tk.Entry(root)
        self.frequency_entry.pack()

        self.add_button = tk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_button.pack()

        self.list_button = tk.Button(root, text="Show Habits", command=self.show_habits)
        self.list_button.pack()

        self.check_button = tk.Button(root, text="Mark Habit Complete", command=self.mark_habit_complete)
        self.check_button.pack()

        self.stats_button = tk.Button(root, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack()

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
