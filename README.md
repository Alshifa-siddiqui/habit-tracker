# Habit Tracker (Python CLI)

A simple CLI-based Habit Tracker built with Python 3.10+.  
Tracks daily and weekly habits with streaks and simple analytics.

## 🚀 Setup Instructions

### 1️⃣ Create Virtual Environment
python -m venv venv  
.\venv\Scripts\activate  

### 2️⃣ Install Requirements
pip install -r requirements.txt  

### 3️⃣ Initialize Database
python  
from src.db import create_table  
create_table()  
exit()  

## 🔧 Usage Examples

### ➕ Add Habit
python main.py add "Workout" "Daily"  
python main.py add "Reading" "Weekly"  

### 📋 Show All Habits
python main.py show  

### ✅ Mark Habit as Completed
python main.py complete "Workout"  

### ❌ Delete a Habit
python main.py delete "Reading"  

### 🔍 Show Habits by Periodicity
python main.py show-by-period "Daily"  

### 🏆 Show Longest Streak
python main.py longest-streak  

## 🧪 Run Unit Tests
pytest  

## 📂 Project Structure
habit-tracker/
├── src/
│ ├── habit.py
│ ├── db.py
│ ├── analytics.py
│ └── cli.py
├── tests/
│ └── test_habit.py
├── data/
│ └── habits.db
├── main.py
├── README.md
├── requirements.txt
└── venv/

## 🔨 Technologies
- Python 3.10+
- SQLite
- Click (CLI Framework)
- Pytest (Testing)
