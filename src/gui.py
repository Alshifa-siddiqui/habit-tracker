import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date, timedelta

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        # Apply a consistent style
        default_font = ("Arial", 12)
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except:
            pass
        self.style.configure('TLabel', font=default_font)
        self.style.configure('TButton', font=default_font)
        self.style.configure('TCheckbutton', font=default_font)
        self.style.configure('TCombobox', font=default_font)

        # Initialize database (use a file like 'habits.db' for persistence, here in-memory for example)
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.setup_database()

        # Load habits into memory list
        self.habits = []
        self.load_habits_from_db()

        # Main menu (Welcome screen) UI
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        welcome_label = ttk.Label(self.main_frame, text="Welcome to Habit Tracker", font=("Arial", 16))
        welcome_label.pack(pady=(0, 15))
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack()
        btn_create = ttk.Button(buttons_frame, text="Create Habit", command=self.open_create_habit_window, width=20)
        btn_view = ttk.Button(buttons_frame, text="View Habits", command=self.open_view_habits_window, width=20)
        btn_progress = ttk.Button(buttons_frame, text="View Progress", command=self.open_progress_window, width=20)
        btn_exit = ttk.Button(buttons_frame, text="Exit", command=self.exit_app, width=20)
        btn_create.grid(row=0, column=0, padx=10, pady=10)
        btn_view.grid(row=0, column=1, padx=10, pady=10)
        btn_progress.grid(row=1, column=0, padx=10, pady=10)
        btn_exit.grid(row=1, column=1, padx=10, pady=10)

    def setup_database(self):
        # Create tables if not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                detail TEXT,
                creation_date TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                timestamp TEXT,
                FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def load_habits_from_db(self):
        # Load all habits into self.habits list
        self.habits = []
        rows = self.cursor.execute("SELECT id, name, frequency, detail, creation_date FROM habits").fetchall()
        for hid, name, freq, detail, creation in rows:
            self.habits.append({
                "id": hid,
                "name": name,
                "freq": freq,
                "detail": detail if detail else "",
                "creation_date": creation
            })

    def open_create_habit_window(self):
        # Window for creating a new habit
        ch_win = tk.Toplevel(self.root)
        ch_win.title("Create Habit")
        ch_win.transient(self.root)  # keep on top of main
        ch_win.grab_set()  # make modal
        frame = ttk.Frame(ch_win, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Habit name input
        ttk.Label(frame, text="Habit Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)

        # Frequency selection
        ttk.Label(frame, text="Frequency:").grid(row=1, column=0, sticky=tk.W, pady=5)
        freq_var = tk.StringVar(value="Daily")
        freq_combo = ttk.Combobox(frame, textvariable=freq_var, values=["Daily", "Weekly", "Monthly"], state="readonly", width=27)
        freq_combo.grid(row=1, column=1, pady=5)
        freq_combo.current(0)

        # Frames for weekly and monthly options
        weekly_frame = ttk.Frame(frame)
        monthly_frame = ttk.Frame(frame)
        # Weekly checkboxes (Monday-Sunday)
        weekday_vars = []
        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekday_names):
            var = tk.IntVar(value=0)
            cb = ttk.Checkbutton(weekly_frame, text=day, variable=var)
            cb.grid(row=0, column=i, padx=2, pady=2)
            weekday_vars.append(var)
        # Monthly checkboxes (1-31)
        month_vars = []
        for idx in range(31):
            var = tk.IntVar(value=0)
            cb = ttk.Checkbutton(monthly_frame, text=str(idx+1), variable=var)
            r = idx // 8
            c = idx % 8
            cb.grid(row=r, column=c, padx=2, pady=2)
            month_vars.append(var)
        # Place frames (hidden by default)
        weekly_frame.grid(row=2, column=1, pady=5, sticky=tk.W)
        monthly_frame.grid(row=2, column=1, pady=5, sticky=tk.W)
        weekly_frame.grid_remove()
        monthly_frame.grid_remove()

        # Handle frequency selection changes to show appropriate options
        def on_freq_change(event=None):
            f = freq_var.get()
            if f == "Weekly":
                weekly_frame.grid()
                monthly_frame.grid_remove()
            elif f == "Monthly":
                monthly_frame.grid()
                weekly_frame.grid_remove()
            else:  # Daily
                weekly_frame.grid_remove()
                monthly_frame.grid_remove()

        freq_combo.bind("<<ComboboxSelected>>", on_freq_change)
        on_freq_change()  # initialize correct view

        # Create habit in database
        def create_habit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Input Error", "Please enter a habit name.")
                return
            frequency = freq_var.get()
            detail = ""
            if frequency == "Weekly":
                days_selected = [weekday_names[i] for i, var in enumerate(weekday_vars) if var.get() == 1]
                if not days_selected:
                    messagebox.showerror("Input Error", "Please select at least one day of the week.")
                    return
                detail = ",".join(days_selected)
            elif frequency == "Monthly":
                dates_selected = [str(i+1) for i, var in enumerate(month_vars) if var.get() == 1]
                if not dates_selected:
                    messagebox.showerror("Input Error", "Please select at least one date of the month.")
                    return
                detail = ",".join(dates_selected)
            creation_date = date.today().strftime("%Y-%m-%d")
            try:
                self.cursor.execute(
                    "INSERT INTO habits(name, frequency, detail, creation_date) VALUES (?, ?, ?, ?)",
                    (name, frequency, detail, creation_date)
                )
                self.conn.commit()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to create habit.\n{e}")
                return
            # Update in-memory list and confirm
            habit_id = self.cursor.lastrowid
            self.habits.append({
                "id": habit_id,
                "name": name,
                "freq": frequency,
                "detail": detail,
                "creation_date": creation_date
            })
            messagebox.showinfo("Habit Created", f"Habit '{name}' created successfully.")
            # Reset form for another entry
            name_entry.delete(0, tk.END)
            freq_var.set("Daily")
            freq_combo.current(0)
            on_freq_change()
            for var in weekday_vars: var.set(0)
            for var in month_vars: var.set(0)

        create_btn = ttk.Button(frame, text="Create", command=create_habit)
        create_btn.grid(row=3, column=1, pady=10, sticky=tk.E)

    def open_view_habits_window(self):
        # Window to view and manage habits
        vh_win = tk.Toplevel(self.root)
        vh_win.title("Your Habits")
        frame = ttk.Frame(vh_win, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        instr_label = ttk.Label(frame, text="Select habits to mark completed or delete. (Select one habit to edit.)")
        instr_label.pack(pady=(0, 5))
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        status_label = ttk.Label(frame, text="", foreground="green")
        status_label.pack(pady=(5, 0))

        habit_checkboxes = []
        def populate_list():
            # Refresh habit list display
            for hb in habit_checkboxes:
                hb["widget"].destroy()
            habit_checkboxes.clear()
            self.load_habits_from_db()  # ensure we have latest data
            for habit in self.habits:
                text = f"{habit['name']} ({habit['freq']})"
                var = tk.IntVar(value=0)
                cb = ttk.Checkbutton(list_frame, text=text, variable=var)
                cb.pack(anchor=tk.W, pady=2)
                habit_checkboxes.append({
                    "id": habit["id"],
                    "name": habit["name"],
                    "freq": habit["freq"],
                    "detail": habit["detail"],
                    "var": var,
                    "widget": cb
                })

        populate_list()

        # Edit selected habit
        def edit_habit():
            selected = [hb for hb in habit_checkboxes if hb["var"].get() == 1]
            if len(selected) != 1:
                messagebox.showerror("Edit Habit", "Please select exactly one habit to edit.")
                return
            habit = selected[0]
            ed_win = tk.Toplevel(vh_win)
            ed_win.title("Edit Habit")
            ed_win.grab_set()
            ed_frame = ttk.Frame(ed_win, padding=20)
            ed_frame.pack(fill=tk.BOTH, expand=True)
            # Pre-fill current values
            ttk.Label(ed_frame, text="Habit Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
            name_entry = ttk.Entry(ed_frame, width=30)
            name_entry.grid(row=0, column=1, pady=5)
            name_entry.insert(0, habit["name"])
            ttk.Label(ed_frame, text="Frequency:").grid(row=1, column=0, sticky=tk.W, pady=5)
            freq_var = tk.StringVar(value=habit["freq"])
            freq_combo = ttk.Combobox(ed_frame, textvariable=freq_var, values=["Daily", "Weekly", "Monthly"], state="readonly", width=27)
            freq_combo.grid(row=1, column=1, pady=5)
            # Weekly & monthly options for editing
            weekly_frame = ttk.Frame(ed_frame)
            monthly_frame = ttk.Frame(ed_frame)
            weekday_vars = []
            for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
                var = tk.IntVar(value=0)
                cb = ttk.Checkbutton(weekly_frame, text=day, variable=var)
                cb.grid(row=0, column=i, padx=2, pady=2)
                weekday_vars.append(var)
            month_vars = []
            for idx in range(31):
                var = tk.IntVar(value=0)
                cb = ttk.Checkbutton(monthly_frame, text=str(idx+1), variable=var)
                r = idx // 8
                c = idx % 8
                cb.grid(row=r, column=c, padx=2, pady=2)
                month_vars.append(var)
            weekly_frame.grid(row=2, column=1, pady=5, sticky=tk.W)
            monthly_frame.grid(row=2, column=1, pady=5, sticky=tk.W)
            # Pre-select current schedule options
            if habit["freq"] == "Weekly":
                days = habit["detail"].split(",") if habit["detail"] else []
                for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
                    if day in days:
                        weekday_vars[i].set(1)
            if habit["freq"] == "Monthly":
                dates_sel = habit["detail"].split(",") if habit["detail"] else []
                for d in dates_sel:
                    try:
                        idx = int(d) - 1
                        if 0 <= idx < 31:
                            month_vars[idx].set(1)
                    except:
                        continue
            # Show relevant frame for current freq
            if habit["freq"] == "Weekly":
                weekly_frame.grid()
                monthly_frame.grid_remove()
            elif habit["freq"] == "Monthly":
                monthly_frame.grid()
                weekly_frame.grid_remove()
            else:  # Daily
                weekly_frame.grid_remove()
                monthly_frame.grid_remove()

            def on_freq_change_local(event=None):
                f = freq_var.get()
                if f == "Weekly":
                    weekly_frame.grid()
                    monthly_frame.grid_remove()
                elif f == "Monthly":
                    monthly_frame.grid()
                    weekly_frame.grid_remove()
                else:
                    weekly_frame.grid_remove()
                    monthly_frame.grid_remove()

            freq_combo.bind("<<ComboboxSelected>>", on_freq_change_local)

            def save_changes():
                new_name = name_entry.get().strip()
                if not new_name:
                    messagebox.showerror("Input Error", "Please enter a habit name.")
                    return
                new_freq = freq_var.get()
                new_detail = ""
                if new_freq == "Weekly":
                    days_selected = [day for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) if weekday_vars[i].get() == 1]
                    if not days_selected:
                        messagebox.showerror("Input Error", "Please select at least one day of the week.")
                        return
                    new_detail = ",".join(days_selected)
                elif new_freq == "Monthly":
                    dates_selected = [str(idx+1) for idx, var in enumerate(month_vars) if var.get() == 1]
                    if not dates_selected:
                        messagebox.showerror("Input Error", "Please select at least one date of the month.")
                        return
                    new_detail = ",".join(dates_selected)
                try:
                    self.cursor.execute(
                        "UPDATE habits SET name=?, frequency=?, detail=? WHERE id=?",
                        (new_name, new_freq, new_detail, habit["id"])
                    )
                    self.conn.commit()
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to update habit.\n{e}")
                    return
                # Update in-memory data and UI
                for h in self.habits:
                    if h["id"] == habit["id"]:
                        h["name"] = new_name
                        h["freq"] = new_freq
                        h["detail"] = new_detail
                        break
                populate_list()
                status_label.config(text=f"Habit '{new_name}' updated.")
                ed_win.destroy()

            save_btn = ttk.Button(ed_frame, text="Save Changes", command=save_changes)
            save_btn.grid(row=3, column=1, pady=10, sticky=tk.E)

        # Delete selected habits (supports multiple selection)
        def delete_habits():
            selected = [hb for hb in habit_checkboxes if hb["var"].get() == 1]
            if not selected:
                messagebox.showerror("Delete Habit", "Please select at least one habit to delete.")
                return
            names = [hb["name"] for hb in selected]
            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete the following habits?\n" + "\n".join(names)
            )
            if not confirm:
                return
            ids = tuple(hb["id"] for hb in selected)
            try:
                if ids:
                    q_marks = ",".join("?" for _ in ids)
                    # Delete associated completions and habits records
                    self.cursor.execute(f"DELETE FROM completions WHERE habit_id IN ({q_marks})", ids)
                    self.cursor.execute(f"DELETE FROM habits WHERE id IN ({q_marks})", ids)
                    self.conn.commit()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete habit(s).\n{e}")
                return
            # Update memory and UI
            id_set = set(ids)
            self.habits = [h for h in self.habits if h["id"] not in id_set]
            populate_list()
            status_label.config(text="Deleted habit(s): " + ", ".join(names))

        # Mark selected habits as completed (logs completion with timestamp)
        def mark_completed():
            selected = [hb for hb in habit_checkboxes if hb["var"].get() == 1]
            if not selected:
                messagebox.showerror("Mark Completed", "Please select at least one habit to mark as completed.")
                return
            for hb in selected:
                hid = hb["id"]
                name = hb["name"]
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    self.cursor.execute("INSERT INTO completions(habit_id, timestamp) VALUES (?, ?)", (hid, ts))
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to record completion for {name}.\n{e}")
            self.conn.commit()
            # Uncheck the boxes after logging completion
            for hb in selected:
                hb["var"].set(0)
            if len(selected) == 1:
                status_label.config(text=f"Marked '{selected[0]['name']}' as completed.")
            else:
                status_label.config(text=f"Marked {len(selected)} habits as completed.")

        # Action buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        edit_btn = ttk.Button(btn_frame, text="Edit", command=edit_habit)
        mark_btn = ttk.Button(btn_frame, text="Mark Completed", command=mark_completed)
        delete_btn = ttk.Button(btn_frame, text="Delete", command=delete_habits)
        edit_btn.grid(row=0, column=0, padx=5)
        mark_btn.grid(row=0, column=1, padx=5)
        delete_btn.grid(row=0, column=2, padx=5)

    def open_progress_window(self):
        # Window to display progress charts
        if not self.habits:
            messagebox.showinfo("No Habits", "No habits available to display progress. Please create a habit first.")
            return
        prog_win = tk.Toplevel(self.root)
        prog_win.title("Progress Tracking")
        prog_frame = ttk.Frame(prog_win, padding=10)
        prog_frame.pack(fill=tk.BOTH, expand=True)
        notebook = ttk.Notebook(prog_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        habit_tab = ttk.Frame(notebook, padding=10)
        overall_tab = ttk.Frame(notebook, padding=10)
        notebook.add(habit_tab, text="Habit Progress")
        notebook.add(overall_tab, text="Overall Stats")

        # Habit selection for individual charts
        ttk.Label(habit_tab, text="Habit:").grid(row=0, column=0, sticky=tk.W)
        habit_names = [h["name"] for h in self.habits]
        selected_habit = tk.StringVar(value=habit_names[0])
        habit_combo = ttk.Combobox(habit_tab, textvariable=selected_habit, values=habit_names, state="readonly")
        habit_combo.grid(row=0, column=1, pady=5, sticky=tk.W)

        # Prepare figures for charts
        fig = None
        canvas = None
        if Figure is not None:
            fig = Figure(figsize=(5, 6))
            fig.add_subplot(211)  # Pie chart subplot
            fig.add_subplot(212)  # Line chart subplot

        def update_charts():
            # Update pie and line charts for the selected habit
            if Figure is None or FigureCanvasTkAgg is None:
                return
            habit_name = selected_habit.get()
            habit_list = [h for h in self.habits if h["name"] == habit_name]
            if not habit_list:
                return
            habit = habit_list[0]
            # Calculate expected occurrences and completions for this habit
            start_date = datetime.strptime(habit["creation_date"], "%Y-%m-%d").date()
            today = date.today()
            end_date = today - timedelta(days=1)
            consider_today = False
            # Get all completion dates for this habit
            comp_rows = self.cursor.execute("SELECT timestamp FROM completions WHERE habit_id=?", (habit["id"],)).fetchall()
            comp_dates = set()
            for (ts,) in comp_rows:
                if ts:
                    try:
                        comp_date = datetime.strptime(ts[:10], "%Y-%m-%d").date()
                        comp_dates.add(comp_date)
                    except:
                        continue
            if today in comp_dates:
                consider_today = True
                end_date = today
            # Determine all scheduled (expected) dates up to end_date
            expected_dates = []
            curr_date = start_date
            while curr_date <= end_date:
                if habit["freq"] == "Daily":
                    expected = True
                elif habit["freq"] == "Weekly":
                    days_of_week = habit["detail"].split(",") if habit["detail"] else []
                    expected = curr_date.strftime("%a") in days_of_week
                elif habit["freq"] == "Monthly":
                    dates_of_month = [d for d in habit["detail"].split(",") if d]
                    expected = str(curr_date.day) in dates_of_month
                else:
                    expected = False
                if expected:
                    expected_dates.append(curr_date)
                curr_date += timedelta(days=1)
            if consider_today and today not in expected_dates:
                expected_dates.append(today)
            expected_dates.sort()
            expected_count = len(expected_dates)
            # Count completions on expected days and compute streaks
            completed_on_expected = 0
            streak_values = []
            streak = 0
            for d in expected_dates:
                if d in comp_dates:
                    completed_on_expected += 1
                    streak += 1
                else:
                    streak = 0
                streak_values.append(streak)
            completed_count = completed_on_expected

            pie_ax = fig.axes[0]
            line_ax = fig.axes[1]
            pie_ax.clear()
            line_ax.clear()
            if expected_count == 0:
                # No data available yet (habit too new)
                pie_ax.text(0.5, 0.5, "No data available", ha='center', va='center')
                line_ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            else:
                incomplete_count = expected_count - completed_count
                labels = ['Completed', 'Missed']
                colors = ['#4caf50', '#f44336']
                pie_ax.pie([completed_count, incomplete_count], labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                pie_ax.set_title('Completion Rate')
                # Line chart for streak over time
                line_ax.plot(range(1, len(streak_values) + 1), streak_values, marker='o', color='#2196f3')
                line_ax.set_title('Streak Over Time')
                line_ax.set_xlabel('Occurrences')
                line_ax.set_ylabel('Streak Length')
                line_ax.set_ylim(0, max(streak_values + [1]) if streak_values else 1)
            fig.tight_layout()
            canvas.draw()

        if Figure is not None:
            canvas = FigureCanvasTkAgg(fig, master=habit_tab)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)
        habit_combo.bind("<<ComboboxSelected>>", lambda e: update_charts())
        update_charts()

        # Overall stats (bar chart comparing completion rates)
        if Figure is not None:
            fig2 = Figure(figsize=(6, 4))
            ax = fig2.add_subplot(111)
            names = []
            percents = []
            for habit in self.habits:
                # Calculate completion percentage for each habit
                start_date = datetime.strptime(habit["creation_date"], "%Y-%m-%d").date()
                today = date.today()
                end_date = today - timedelta(days=1)
                comp_rows = self.cursor.execute("SELECT timestamp FROM completions WHERE habit_id=?", (habit["id"],)).fetchall()
                comp_dates = set()
                for (ts,) in comp_rows:
                    if ts:
                        try:
                            comp_date = datetime.strptime(ts[:10], "%Y-%m-%d").date()
                            comp_dates.add(comp_date)
                        except:
                            continue
                expected_dates = []
                curr_date = start_date
                while curr_date <= end_date:
                    add = False
                    if habit["freq"] == "Daily":
                        add = True
                    elif habit["freq"] == "Weekly":
                        days_of_week = habit["detail"].split(",") if habit["detail"] else []
                        if curr_date.strftime("%a") in days_of_week:
                            add = True
                    elif habit["freq"] == "Monthly":
                        dom_list = [d for d in habit["detail"].split(",") if d]
                        if str(curr_date.day) in dom_list:
                            add = True
                    if add:
                        expected_dates.append(curr_date)
                    curr_date += timedelta(days=1)
                expected_count = len(expected_dates)
                if expected_count == 0:
                    # Skip habits with no expected occurrences yet
                    continue
                completed_count = sum(1 for d in expected_dates if d in comp_dates)
                percent = (completed_count / expected_count) * 100 if expected_count > 0 else 0
                names.append(habit["name"])
                percents.append(percent)
            if names:
                x_pos = range(len(names))
                bars = ax.bar(x_pos, percents, color='#2196f3')
                ax.set_ylabel('Completion %')
                ax.set_ylim(0, 100)
                ax.set_xticks(list(x_pos))
                ax.set_xticklabels(names, rotation=45, ha='right')
                ax.set_title('Habit Completion Rates')
                # Annotate each bar with percentage
                for i, bar in enumerate(bars):
                    h = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2.0, h + 1, f'{h:.1f}%', ha='center', va='bottom', fontsize=9)
                fig2.tight_layout()
            else:
                ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            canvas2 = FigureCanvasTkAgg(fig2, master=overall_tab)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def exit_app(self):
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
