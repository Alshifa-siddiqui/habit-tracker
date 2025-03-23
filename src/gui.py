import sys
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from database import HabitDatabase
from analytics import HabitAnalytics


class HabitTrackerGUI:
    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x550")
        self.root.configure(bg="#F8F9FA")
        
        self.db = HabitDatabase()
        self.analytics = HabitAnalytics()

        # Fonts
        self.font_title = ("Montserrat", 16, "bold")
        self.font_normal = ("Montserrat", 12)

        # Create Welcome Screen
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Show the welcome screen with main options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Habit Tracker", font=self.font_title, bg="#F8F9FA").pack(pady=20)

        tk.Button(self.root, text="Create a Habit", font=self.font_normal, bg="#28A745", fg="white", 
                  command=self.create_habit_screen, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="View Habits", font=self.font_normal, bg="#007BFF", fg="white",
                  command=self.show_habits, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="View Progress", font=self.font_normal, bg="#FFB703", fg="black",
                  command=self.view_progress, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="Exit", font=self.font_normal, bg="#DC3545", fg="white", 
                  command=self.root.quit, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

    def create_habit_screen(self):
        """Screen to add a new habit."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Create a Habit", font=self.font_title, bg="#F8F9FA").pack(pady=20)

        tk.Label(self.root, text="Habit Name:", font=self.font_normal, bg="#F8F9FA").pack()
        self.habit_entry = tk.Entry(self.root, font=self.font_normal)
        self.habit_entry.pack(pady=5, padx=20, fill="x")

        tk.Label(self.root, text="Frequency:", font=self.font_normal, bg="#F8F9FA").pack()
        self.frequency_var = tk.StringVar(self.root)
        self.frequency_var.set("Daily")  
        tk.OptionMenu(self.root, self.frequency_var, "Daily", "Weekly", "Monthly").pack(pady=5)

        tk.Button(self.root, text="Next", font=self.font_normal, bg="#007BFF", fg="white", 
                  command=self.handle_habit_creation, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="Back", font=self.font_normal, bg="#6C757D", fg="white", 
                  command=self.create_welcome_screen, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

    def handle_habit_creation(self):
        """Handle different habit frequencies."""
        name = self.habit_entry.get().strip()
        frequency = self.frequency_var.get()

        if not name:
            messagebox.showwarning("Warning", "Please enter a habit name.")
            return
        
        self.db.add_habit(name, frequency)
        messagebox.showinfo("Success", f"Habit '{name}' created successfully!")
        self.create_welcome_screen()

    def view_progress(self):
        """Show habit progress using charts."""
        habits = self.db.get_habits()
        if not habits:
            messagebox.showinfo("Progress", "No habits found.")
            return

        habit_names = [habit[1] for habit in habits]
        completion_rates = [self.db.get_completion_rate(habit[0]) for habit in habits]

        # Pie Chart
        fig1, ax1 = plt.subplots()
        ax1.pie(completion_rates, labels=habit_names, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.title("Completion Rate")

        # Line Chart
        fig2, ax2 = plt.subplots()
        ax2.plot(habit_names, completion_rates, marker='o', linestyle='-', color='b')
        plt.xticks(rotation=45)
        plt.title("Habit Progress Over Time")
        plt.xlabel("Habits")
        plt.ylabel("Completion %")

        # Display Charts
        plt.show()

    def show_habits(self):
        """Display all stored habits in a message box."""
        habits = self.db.get_habits()
        if not habits:
            messagebox.showinfo("Tracked Habits", "No habits found.")
            return
        
        habit_list = "\n".join([f"{habit[1]} ({habit[2]})" for habit in habits])
        messagebox.showinfo("Tracked Habits", habit_list)


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
