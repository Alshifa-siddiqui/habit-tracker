# 📋 IU Habit Tracker App

A command-line Python application to help users track daily and weekly habits, analyze streaks, and stay consistent.  
Developed using Object-Oriented and Functional Programming principles with SQLite for persistence.

## 📑 Table of Contents
1. About the Project  
2. Technologies Used  
3. Project Structure  
4. How to Run  
5. Features  
6. UML Class Diagram  
7. Example Usage  
8. License  

## 📌 About the Project
This CLI-based Habit Tracker allows users to:  
- Create, update, and delete daily and weekly habits.  
- Track progress with completion streaks.  
- Analyze habits through periodicity filters and reports.  
- Store all data persistently using SQLite.  

## 🛠️ Technologies Used
- **Python 3.11**  
- **SQLite** for data storage  
- **Click** for CLI interaction  
- **Pytest** for unit testing  

## 📂 Project Structure
habit-tracker/
├── data/
├── src/
│ ├── analytics.py
│ ├── cli.py
│ ├── db.py
│ ├── habit.py
├── tests/
│ ├── test_habit.py
├── main.py
├── README.md
├── requirements.txt

- `src/`: Core application logic (habit management, CLI, analytics, database)  
- `tests/`: Unit tests using Pytest  
- `main.py`: Entry point  
- `requirements.txt`: Project dependencies  

## 🚀 How to Run
1️⃣ Clone the repo:  
```bash
git clone https://github.com/Alshifa-siddiqui/habit-tracker.git
cd habit-tracker

2️⃣ Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux

3️⃣ Install dependencies:
pip install -r requirements.txt

4️⃣ Run the app:python main.py

💡 Example CLI Commands:
python main.py add Workout Daily
python main.py complete Workout
python main.py show
python main.py longest-streak

✨ Features
Track daily/weekly habits

Analyze longest streaks

Periodicity filtering

SQLite persistent storage

CLI interaction via Click

Unit tests with Pytest

📝 UML Class Diagram
![UML Diagram](./assets/uml.png)

📸 Example CLI Output
### Main Menu
![Main Menu](assets/cli/CODE.png)

### Example Output

📄 License
MIT License
