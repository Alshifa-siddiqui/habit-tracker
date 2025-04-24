# 🧿 Habit Tracker of Shadows 🧿  
_“Track your habits. Master your fate.”_  

> A CLI-based habit tracking system forged in Python, built to slay inconsistency and summon discipline from the abyss.

![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)

---

## 🖤 Table of Contents  
- ✨ Features  
- ⚙️ Project Structure  
- 🧩 Functionality  
- 💻 Installation & Setup  
- 🧪 Running Tests  
- 🕹️ Usage (CLI Commands)  
- 🗃️ Technologies Used  
- 🔮 Future Enhancements  

---

## ✨ Features  

- ✅ Create daily or weekly habits  
- ✅ Track progress, streaks, broken streaks  
- ✅ Dynamic performance analysis & visualizations  
- ✅ Generate reports  
- ✅ View most consistent & most struggled habits  
- ✅ Easily update descriptions, periods, and streaks  
- ✅ Persist data via SQLite + Pickle  
- ✅ Optimized to handle large-scale data  
- ✅ 36 Automated Unit Tests ✅

---

## ⚙️ Project Structure  

```
habit-tracker/
│
├── src/                        # All core logic lives here
│   ├── CLI.py                 # Command Line Interface entry point
│   ├── habit.py               # Habit class with logic & calculations
│   ├── habitDB.py             # Database operations & validation
│   ├── analysis.py            # Habit performance analysis
│   ├── Dates_Persistence.py   # Handles Pickle for date tracking
│   └── visualization.py       # (Optional) Plotting and reports
│
├── tests/                     # Pytest test suite (36 tests!)
│   ├── test_habit.py
│   ├── test_habitdb.py
│   ├── test_analysis.py
│   └── test_preformance.py
│
├── assets/                    # Images, screenshots, sample reports
├── docs/                      # Documentation and notes
├── habits.db                  # SQLite database
├── requirements.txt           # Dependencies
├── README.md                  # This file right here
└── .gitignore                 # Exclude db, venv, cache, etc.
```

---

## 🧩 Functionality Overview  

| Command / Method                     | Description |
|-------------------------------------|-------------|
| `create_habit`                      | Create a new habit with details |
| `delete_habit`                      | Remove a habit |
| `habit_is_done_today`               | Mark today's progress |
| `update_status_streak`             | Update streak & status |
| `get_completed_habits`             | Fetch completed habits |
| `get_incomplete_habits`            | Fetch habits still in progress |
| `get_streak` / `get_broken_count`  | Retrieve habit performance stats |
| `longest_run_streak_for_a_given_habit` | See longest streak |
| `calculate_completion_rate`        | Completion analytics |
| `get_most_consistent_habits`       | Identify strongest habits |
| `get_most_struggled_habits`        | See which habits need care |
| `delete_all_habits`                | Burn it all 🔥 (for resets) |

---

## 💻 Installation & Setup  

### 🧙 Requirements

- Python 3.11+  
- pip  
- virtualenv (optional, but encouraged)

### 🛠️ Setup Steps

```bash
# Clone the shadow repository
git clone https://github.com/your-darkness/habit-tracker.git
cd habit-tracker

# (Optional) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate    # On Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Running Tests  

36 unit tests. No mercy. No leaks.  
💀 Full test coverage.  

```bash

### 🌱 Load Sample Habits (Optional but Recommended)

To quickly test analytics and reports with pre-filled data, run:

```bash
python src/seed_habits.py

# Run all tests
pytest tests/
```

---

## 🕹️ How to Use (CLI)  

Launch the command-line interface:

```bash
python src/CLI.py
```

Choose from the dark menu:
```
1. Create a new habit
2. Delete a habit
3. Mark a habit as completed today
4. View habit streak
5. View habit broken count
...
19. View most consistent habit
20. View most struggled habit
23. Generate a progress report
26. Exit the realm
```

---

## 🗃️ Technologies Used  

| Tool            | Use                          |
|-----------------|------------------------------|
| 🐍 Python 3.11   | Core language                |
| 🧠 SQLite3       | Habit storage backend        |
| 🧼 Pickle        | Persistent date tracking     |
| 🔍 Pytest        | Unit testing                 |
| 📊 Matplotlib    | Visualizing progress (soon)  |

---

## 🔮 Future Enhancements  

- 📈 Graphical data visualizations  
- 🌐 GUI-based user interface  
- 🗣️ Voice-based logging  
- 🌍 Cloud sync for multiple users  
- 📱 Mobile app integration  

---


