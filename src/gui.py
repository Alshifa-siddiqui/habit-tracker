import sys
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from database import HabitDatabase
from analytics import HabitAnalytics


class HabitTrackerGUI:
    """GUI for the Habit Tracker application."""

    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x500")
        self.root.configure(bg="#F8F9FA")
        
        self.db = HabitDatabase()
        self.analytics = HabitAnalytics()

        self.font_title = ("Montserrat", 16, "bold")
        self.font_normal = ("Montserrat", 12)

        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Show the welcome screen with main options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Habit Tracker!", font=self.font_title, bg="#F8F9FA").pack(pady=20)

        tk.Button(self.root, text="Create a Habit", font=self.font_normal, bg="#28A745", fg="white",
                  command=self.create_habit_screen).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="View Habits", font=self.font_normal, bg="#007BFF", fg="white",
                  command=self.show_habits).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="Track Progress", font=self.font_normal, bg="#17A2B8", fg="white",
                  command=self.view_progress).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="Exit", font=self.font_normal, bg="#DC3545", fg="white",
                  command=self.root.quit).pack(pady=10, fill="x", padx=50)

    def create_habit_screen(self):
        """Screen to add a new habit with timing and frequency options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Create a Habit", font=self.font_title, bg="#F8F9FA").pack(pady=20)

        tk.Label(self.root, text="Habit Name:", font=self.font_normal, bg="#F8F9FA").pack()
        self.habit_entry = tk.Entry(self.root, font=self.font_normal)
        self.habit_entry.pack(pady=5, padx=20, fill="x")

        tk.Label(self.root, text="Frequency:", font=self.font_normal, bg="#F8F9FA").pack()
        self.frequency_var = tk.StringVar()
        self.frequency_var.set("Daily")
        tk.OptionMenu(self.root, self.frequency_var, "Daily", "Weekly", "Monthly").pack(pady=5)

        tk.Label(self.root, text="Time (12-hour format e.g., 02:00 PM - 03:00 PM):", font=self.font_normal, bg="#F8F9FA").pack()
        self.time_entry = tk.Entry(self.root, font=self.font_normal)
        self.time_entry.pack(pady=5, padx=20, fill="x")

        tk.Button(self.root, text="Create Habit", font=self.font_normal, bg="#007BFF", fg="white",
                  command=self.handle_habit_creation).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="Back", font=self.font_normal, bg="#6C757D", fg="white",
                  command=self.create_welcome_screen).pack(pady=10, fill="x", padx=50)

    def handle_habit_creation(self):
        """Handle different habit frequencies and time."""
        name = self.habit_entry.get().strip()
        frequency = self.frequency_var.get()
        time = self.time_entry.get().strip()

        if not name or not time:
            messagebox.showwarning("Warning", "Please enter all details.")
            return

        self.db.add_habit(name, frequency, time)
        messagebox.showinfo("Success", f"Habit '{name}' added with time '{time}'!")
        self.create_welcome_screen()

    def show_habits(self):
        """Display all stored habits with completion tracking."""
        habits = self.db.get_habits()
        habit_list = "\n".join([f"{habit[1]} ({habit[2]}) - Time: {habit[3]}" for habit in habits])
        messagebox.showinfo("Tracked Habits", habit_list if habit_list else "No habits found.")

    def view_progress(self):
        """Display progress using pie chart, bar chart, and line chart."""
        habits = self.db.get_habits()
        if not habits:
            messagebox.showwarning("No Data", "No habits found to track progress.")
            return

        completion_rates = [self.db.get_completion_rate(habit[0]) for habit in habits]
        labels = [habit[1] for habit in habits]

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        ax1.pie(completion_rates, labels=labels, autopct='%1.1f%%')
        ax1.set_title("Completion Percentage")

        ax2.bar(labels, completion_rates, color='skyblue')
        ax2.set_title("Comparison of Habit Completion")

        ax3.plot(labels, completion_rates, marker='o', linestyle='-', color='green')
        ax3.set_title("Progress Over Time")

        plt.tight_layout()
        plt.show()

    def auto_mark_missed_tasks(self):
        """Check for habits that were not completed within 24 hours and mark them as missed."""
        habits = self.db.get_habits()
        now = datetime.now()

        for habit in habits:
            last_completed = self.db.get_last_completion_date(habit[0])
            if last_completed and (now - last_completed).days >= 1:
                self.db.mark_habit_missed(habit[0])

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
