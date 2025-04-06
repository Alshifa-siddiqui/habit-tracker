# 🌒 Habit Tracker CLI — Rule Your Routines from the Terminal

> “Discipline is choosing between what you want *now* and what you want *most*.”  
> Welcome to your command-line sanctuary of self-mastery.

---

## 🧩 What Is This?

**Habit Tracker CLI** is your digital spellbook for building better habits — created entirely in Python using **Object-Oriented Programming** (OOP) and a dash of **functional magic** ✨.

From tracking daily rituals to analyzing weekly progress, everything is at your fingertips — no mouse, no GUI, just pure, minimalist power.

---

## ✨ Why Use It?

- 👑 Because GUIs are overrated.
- 🧠 Because discipline should be **data-driven**.
- 🔮 Because it was crafted with code, caffeine, and chaos.

This app was developed as part of the IU portfolio assignment for **Object-Oriented and Functional Programming** — but designed like a product worth publishing.

---

## 🚀 Features at a Glance

| ⚔️ Feature             | 💬 Description |
|------------------------|----------------|
| 🛠️ Create Habits       | Daily or weekly |
| 📝 Edit/Delete Habits  | Refine or remove |
| 📆 Check-In Logging    | Record completion dates |
| 📊 Analytics           | Functional programming magic to analyze streaks |
| 💾 Persistent Storage  | Data saved in SQLite automatically |
| 🧪 Unit Tested         | Includes unit tests for reliability |

---

## 🛠️ Tech Behind the Magic

- **Python 3.x**
- **SQLite** (`sqlite3`)
- **Functional Programming**: Analytics logic
- **Object-Oriented Design**: Habit + HabitDB classes
- **Unittest** for testing modules

---

## 🧙 How to Summon the Tracker (Installation)

First, clone the repository:

```bash
git clone https://github.com/Alshifa-siddiqui/habit-tracker.git
cd habit-tracker

Then install dependencies
pip install -r requirements.txt

🧰 How to Use It
👉 From the root of the project:
python src/CLI.py


You’ll be guided via text-based prompts to:

Add a new habit

Log a check-in

View your current habits

Analyze performance via terminal dashboards

🔍 Folder Spellbook
habit-tracker/
├── src/
│   ├── CLI.py                  # Main command-line interface
│   ├── HabitDB.py              # SQLite + Habit logic
│   ├── habit.py                # Habit class (OOP)
│   ├── analytics.py            # Functional performance analysis
│   ├── dates_persistance.py    # Save/load habit check-in dates
│   └── __init__.py
├── tests/
│   ├── test_habitdb.py
│   ├── test_analytics.py
│   └── ...
├── README.md
├── requirements.txt
├── setup.py
├── habits.db                   # Auto-generated database

🧪 Running the Tests
Because we don’t trust code without tests, do:
cd tests
python -m unittest discover

You’ll see output confirming all habit/database/analytics modules are functioning properly.
