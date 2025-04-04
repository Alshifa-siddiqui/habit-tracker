import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.scrolledtext import ScrolledText
from database import get_db, create_habit, add_completion, delete_habit
from analytics import get_all_habits, get_habits_by_periodicity, get_longest_streak

class HabitTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 HabitHero - Smart Habit Tracker")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Custom Colors
        self.bg_color = "#2D2D2D"
        self.accent_color = "#4CAF50"
        self.text_color = "#FFFFFF"
        
        self.root.configure(bg=self.bg_color)
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TButton", background=self.accent_color, foreground="black")
        self.style.configure("Treeview", background="#404040", fieldbackground="#404040", foreground="white")
        
        # Main Container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header = ttk.Frame(self.main_frame)
        self.header.pack(fill=tk.X)
        
        ttk.Label(self.header, text="HabitHero", font=("Helvetica", 24, "bold")).pack(side=tk.LEFT)
        
        # Add Habit Section
        self.add_habit_frame = ttk.Frame(self.main_frame)
        self.add_habit_frame.pack(fill=tk.X, pady=10)
        
        self.task_entry = ttk.Entry(self.add_habit_frame, width=30, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        self.periodicity_var = tk.StringVar(value="daily")
        ttk.Radiobutton(self.add_habit_frame, text="Daily", variable=self.periodicity_var, 
                       value="daily", style="TRadiobutton").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.add_habit_frame, text="Weekly", variable=self.periodicity_var,
                       value="weekly", style="TRadiobutton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.add_habit_frame, text="➕ Create Habit", command=self.create_habit).pack(side=tk.LEFT, padx=10)
        
        # Habits List
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Task", "Periodicity"), show="headings",
                                selectmode="browse", style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Periodicity", text="Periodicity")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Task", width=400)
        self.tree.column("Periodicity", width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Action Buttons
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(self.btn_frame, text="✅ Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="🗑️ Delete Habit", command=self.delete_habit).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="📊 Show Analytics", command=self.show_analytics).pack(side=tk.LEFT, padx=5)
        
        self.refresh_list()

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        with get_db() as conn:
            habits = get_all_habits(conn)
            for habit in habits:
                self.tree.insert("", "end", values=(habit['id'], habit['task'], habit['periodicity']))
    
    def create_habit(self):
        task = self.task_entry.get()
        if not task:
            messagebox.showerror("Error", "Please enter a habit name!")
            return
            
        periodicity = self.periodicity_var.get()
        try:
            with get_db() as conn:
                create_habit(conn, task, periodicity)
            self.task_entry.delete(0, tk.END)
            self.refresh_list()
            messagebox.showinfo("Success", f"Habit '{task}' created!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Rest of the methods remain similar to previous version with style enhancements

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()