import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.database import HabitDatabase

class HabitTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f9ff")
        self.db = HabitDatabase()
        self.habit_details = {}
        self.create_main_frame()
        self.refresh_habits_list()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="#f0f9ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Panel: Habit List
        list_frame = tk.Frame(self.main_frame, bg="#f0f9ff")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        header_canvas = tk.Canvas(list_frame, height=50, bg="#f0f9ff", highlightthickness=0)
        header_canvas.pack(fill=tk.X)
        header_canvas.create_text(50, 5, text="Habits", font=("Arial", 14, "bold"), anchor="nw")

        self.habit_listbox = tk.Listbox(list_frame, font=("Arial", 12), bg="#e3f2fd", selectmode=tk.SINGLE)
        self.habit_listbox.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.habit_listbox.bind("<<ListboxSelect>>", self.on_habit_select)

        add_btn = tk.Button(list_frame, text="+ Add Habit", font=("Arial", 12, "bold"), 
                           bg="#64b5f6", fg="white", command=self.show_add_form)
        add_btn.pack(pady=10, fill=tk.X)

        # Right Panel: Habit Details
        detail_frame = tk.Frame(self.main_frame, bg="#f0f9ff", relief=tk.RIDGE)
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.name_detail = tk.Label(detail_frame, text="", font=("Arial", 12), bg="#f0f9ff")
        self.name_detail.pack(anchor="nw", pady=(10, 0))
        self.freq_detail = tk.Label(detail_frame, text="", font=("Arial", 12), bg="#f0f9ff")
        self.freq_detail.pack(anchor="nw")
        self.count_detail = tk.Label(detail_frame, text="", font=("Arial", 12), bg="#f0f9ff")
        self.count_detail.pack(anchor="nw")
        self.current_streak_detail = tk.Label(detail_frame, text="", font=("Arial", 12), bg="#f0f9ff")
        self.current_streak_detail.pack(anchor="nw")
        self.longest_streak_detail = tk.Label(detail_frame, text="", font=("Arial", 12), bg="#f0f9ff")
        self.longest_streak_detail.pack(anchor="nw")

        btn_frame = tk.Frame(detail_frame, bg="#f0f9ff")
        btn_frame.pack(anchor="nw", pady=10)
        self.complete_btn = tk.Button(btn_frame, text="Mark Completed", font=("Arial", 10, "bold"),
                                     bg="#66bb6a", fg="white", command=self.mark_completed)
        self.complete_btn.grid(row=0, column=0, padx=5)
        self.edit_btn = tk.Button(btn_frame, text="Edit", font=("Arial", 10, "bold"),
                                 bg="#ffa726", fg="white", command=self.show_edit_form)
        self.edit_btn.grid(row=0, column=1, padx=5)
        self.delete_btn = tk.Button(btn_frame, text="Delete", font=("Arial", 10, "bold"),
                                   bg="#ef5350", fg="white", command=self.delete_habit)
        self.delete_btn.grid(row=0, column=2, padx=5)

    def refresh_habits_list(self, select_name=None):
        self.habit_listbox.delete(0, tk.END)
        self.habit_details.clear()
        habits = self.db.get_habits()
        if not habits:
            self.set_detail_message("No habits found. Add a habit to start!")
            return
        for habit in sorted(habits, key=lambda h: h['name']):
            self.habit_listbox.insert(tk.END, habit['name'])
            self.habit_details[habit['name']] = habit
        if select_name:
            index = list(self.habit_details.keys()).index(select_name)
            self.habit_listbox.selection_set(index)
            self.show_habit_details(select_name)

    def show_habit_details(self, name):
        habit = self.habit_details.get(name)
        if not habit:
            return
        self.name_detail.config(text=f"Name: {habit['name']}")
        freq_text = f"Frequency: {habit['frequency']}"
        if habit['frequency'] == "Weekly" and habit['day_of_week']:
            freq_text += f" ({habit['day_of_week']})"
        elif habit['frequency'] == "Monthly" and habit['date_of_month']:
            freq_text += f" ({habit['date_of_month']})"
        self.freq_detail.config(text=freq_text)
        self.count_detail.config(text=f"Completed: {habit['completed_count']}")
        self.current_streak_detail.config(text=f"Current Streak: {habit['current_streak']}")
        self.longest_streak_detail.config(text=f"Longest Streak: {habit['longest_streak']}")
        self.complete_btn.config(state=tk.NORMAL)
        self.edit_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)

    def show_add_form(self):
        self.open_form_window("Add Habit")

    def show_edit_form(self):
        selected = self.habit_listbox.curselection()
        if not selected:
            return
        name = self.habit_listbox.get(selected[0])
        habit = self.habit_details.get(name)
        self.open_form_window("Edit Habit", habit)

    def open_form_window(self, title, habit=None):
        self.main_frame.pack_forget()
        form_frame = tk.Frame(self.root, bg="#fffde7", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Habit Name:", bg="#fffde7").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(form_frame, font=("Arial", 12))
        name_entry.grid(row=0, column=1, pady=5)

        frequency_var = tk.StringVar(value="Daily" if not habit else habit['frequency'])
        tk.Radiobutton(form_frame, text="Daily", variable=frequency_var, value="Daily", 
                      bg="#fffde7", command=lambda: self.toggle_frequency("Daily")).grid(row=1, column=1, sticky="w")
        tk.Radiobutton(form_frame, text="Weekly", variable=frequency_var, value="Weekly", 
                      bg="#fffde7", command=lambda: self.toggle_frequency("Weekly")).grid(row=2, column=1, sticky="w")
        tk.Radiobutton(form_frame, text="Monthly", variable=frequency_var, value="Monthly", 
                      bg="#fffde7", command=lambda: self.toggle_frequency("Monthly")).grid(row=3, column=1, sticky="w")

        days_listbox = tk.Listbox(form_frame, selectmode=tk.MULTIPLE, height=7)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            days_listbox.insert(tk.END, day)
        dates_listbox = tk.Listbox(form_frame, selectmode=tk.MULTIPLE, height=10)
        for date in range(1, 32):
            dates_listbox.insert(tk.END, str(date))

        if habit:
            name_entry.insert(0, habit['name'])
            if habit['frequency'] == "Weekly" and habit['day_of_week']:
                selected_days = habit['day_of_week'].split(",")
                for day in selected_days:
                    if day.strip() in days:
                        days_listbox.selection_set(days.index(day.strip()))
            elif habit['frequency'] == "Monthly" and habit['date_of_month']:
                selected_dates = habit['date_of_month'].split(",")
                for date in selected_dates:
                    if date.strip().isdigit():
                        dates_listbox.selection_set(int(date.strip()) - 1)

        def save():
            name = name_entry.get().strip()
            frequency = frequency_var.get()
            days = ",".join([days_listbox.get(i) for i in days_listbox.curselection()]) if frequency == "Weekly" else None
            dates = ",".join([dates_listbox.get(i) for i in dates_listbox.curselection()]) if frequency == "Monthly" else None
            try:
                if habit:
                    self.db.update_habit(habit['name'], name, frequency, days, dates)
                else:
                    self.db.add_habit(name, frequency, days, dates)
                self.refresh_habits_list(name)
                form_frame.destroy()
                self.main_frame.pack()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(form_frame, text="Save", command=save).grid(row=10, column=0, pady=20)
        tk.Button(form_frame, text="Cancel", command=lambda: [form_frame.destroy(), self.main_frame.pack()]).grid(row=10, column=1)

    def toggle_frequency(self, frequency):
        # Logic to show/hide days/dates listboxes (similar to your previous code)
        pass

    def mark_completed(self):
        selected = self.habit_listbox.curselection()
        if not selected:
            return
        name = self.habit_listbox.get(selected[0])
        try:
            self.db.mark_habit_completed(name)
            self.refresh_habits_list(name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_habit(self):
        selected = self.habit_listbox.curselection()
        if not selected:
            return
        name = self.habit_listbox.get(selected[0])
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            self.db.delete_habit(name)
            self.refresh_habits_list()

    def set_detail_message(self, msg):
        self.name_detail.config(text=msg)
        self.freq_detail.config(text="")
        self.count_detail.config(text="")
        self.current_streak_detail.config(text="")
        self.longest_streak_detail.config(text="")
        self.complete_btn.config(state=tk.DISABLED)
        self.edit_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def on_habit_select(self, event):
        if self.habit_listbox.curselection():
            self.show_habit_details(self.habit_listbox.get(self.habit_listbox.curselection()[0]))
if __name__ == "__main__":
        root = tk.Tk()
        app = HabitTrackerGUI(root)
        root.mainloop()