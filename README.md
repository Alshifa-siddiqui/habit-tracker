# Habit Tracker (Python CLI)

A simple CLI-based Habit Tracker built with Python 3.10+.  
Tracks daily and weekly habits with streaks and simple analytics.

## 🚀 Setup Instructions

python -m venv venv  
.\venv\Scripts\activate  
pip install -r requirements.txt  

python  
from src.db import create_table  
create_table()  
exit()  

## 🔧 Usage Examples

python main.py add "Workout" "Daily"  
python main.py show  
python main.py complete "Workout"  
python main.py delete "Reading"  
python main.py show-by-period "Daily"  
python main.py longest-streak  

## 🧪 Run Unit Tests
pytest  

## 📂 Project Structure
habit-tracker/  
├── src/  
│   ├── habit.py  
│   ├── db.py  
│   ├── analytics.py  
│   └── cli.py  
├── tests/  
│   └── test_habit.py  
├── data/  
│   └── habits.db  
├── main.py  
├── README.md  
├── requirements.txt  
└── venv/  

## 🔨 Technologies
- Python 3.10+
- SQLite
- Click (CLI Framework)
- Pytest (Testing)
