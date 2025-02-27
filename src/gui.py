import sys
import os
import tkinter as tk
from tkinter import messagebox
from src.database import HabitDatabase
from src.analytics import HabitAnalytics

class HabitTrackerGUI:
    def __init__(self, root):
        """Initialize the GUI and connect to the database."""
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x500")
        self.root.configure(bg="#F8F9FA")
        
        self.db = HabitDatabase()
        self.analytics = HabitAnalytics()

        # Fonts
        self.font_title = ("Montserrat", 16, "bold")
        self.font_normal = ("Montserrat", 12)

        # Create Welcome Screen
        self.create_welcome_screen()
    
    def delete_habit(self):
        """Delete a habit from the database."""
    habit_id = self.habit_entry.get().strip()
    
    if habit_id.isdigit():
        habit_id = int(habit_id)
        self.db.remove_habit(habit_id)  # Use remove_habit instead of delete_habit
        messagebox.showinfo("Success", f"Habit {habit_id} deleted successfully!")
        self.create_welcome_screen()  # Refresh UI
    else:
        messagebox.showwarning("Warning", "Please enter a valid habit ID.")



    def create_welcome_screen(self):
        """Show the welcome screen with main options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        delete_btn = tk.Button(self.root, text="Delete Habit", font=self.font_normal, 
                       command=self.delete_habit, bg="red", fg="white")
        delete_btn.pack(pady=10)


        tk.Label(self.root, text="Habit Tracker", font=self.font_title, bg="#F8F9FA").pack(pady=20)

        tk.Button(self.root, text="Create a Habit", font=self.font_normal, bg="#28A745", fg="white", 
                  command=self.create_habit_screen, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

        tk.Button(self.root, text="View Habits", font=self.font_normal, bg="#007BFF", fg="white",
                  command=self.show_habits, padx=10, pady=8).pack(pady=10, fill="x", padx=50)

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
        self.frequency_var.set("Daily")  # Default value
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
        
        if frequency == "Daily":
            self.db.add_habit(name, "Daily")
            messagebox.showinfo("Success", f"Habit '{name}' created as a Daily habit!")
            self.create_welcome_screen()
        elif frequency == "Weekly":
            self.select_weekly_schedule(name)
        elif frequency == "Monthly":
            self.select_monthly_schedule(name)

    def select_weekly_schedule(self, name):
        """Popup for selecting multiple days for a weekly habit."""
        weekly_popup = tk.Toplevel(self.root)
        weekly_popup.title("Select Weekly Schedule")
        weekly_popup.geometry("300x350")

        tk.Label(weekly_popup, text="Select Days:", font=self.font_title).pack(pady=10)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        selected_days = {}

        for day in days:
            var = tk.IntVar()
            chk = tk.Checkbutton(weekly_popup, text=day, font=self.font_normal, variable=var)
            chk.pack(anchor="w", padx=20)
            selected_days[day] = var

        def confirm_weekly():
            """Save the selected days."""
            chosen_days = [day for day, var in selected_days.items() if var.get() == 1]
            if not chosen_days:
                messagebox.showwarning("Warning", "Please select at least one day.")
                return

            self.db.add_habit(name, f"Weekly: {', '.join(chosen_days)}")
            messagebox.showinfo("Success", f"Habit '{name}' scheduled for {', '.join(chosen_days)}.")
            weekly_popup.destroy()
            self.create_welcome_screen()

        tk.Button(weekly_popup, text="Confirm", font=self.font_normal, bg="#28A745", fg="white",
                  command=confirm_weekly).pack(pady=10)

    def select_monthly_schedule(self, name):
        """Popup for selecting a specific day of the month."""
        monthly_popup = tk.Toplevel(self.root)
        monthly_popup.title("Select Monthly Schedule")
        monthly_popup.geometry("300x200")

        tk.Label(monthly_popup, text="Select a Date:", font=self.font_title).pack(pady=10)

        self.date_var = tk.StringVar()
        self.date_var.set("1")  # Default value
        tk.OptionMenu(monthly_popup, self.date_var, *[str(i) for i in range(1, 32)]).pack(pady=5)

        def confirm_monthly():
            """Save the selected date."""
            date_selected = self.date_var.get()
            self.db.add_habit(name, f"Monthly: {date_selected}")
            messagebox.showinfo("Success", f"Habit '{name}' scheduled for day {date_selected} of each month.")
            monthly_popup.destroy()
            self.create_welcome_screen()

        tk.Button(monthly_popup, text="Confirm", font=self.font_normal, bg="#28A745", fg="white",
                  command=confirm_monthly).pack(pady=10)

    def show_habits(self):
        """Display all stored habits in a message box."""
        habits = self.db.get_habits()
        habit_list = "\n".join([f"ID: {habit[0]} - {habit[1]} ({habit[2]})" for habit in habits])
        messagebox.showinfo("Tracked Habits", habit_list if habit_list else "No habits found.")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
