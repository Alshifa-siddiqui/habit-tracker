# Habit Tracker

A **university project** for the course **"Object-Oriented and Functional Programming with Python"**.

This application is designed to help users **track their habits**, monitor progress, and analyze statistics like streaks and missed habits. Built using **Python 3.12**, it follows best practices in software development, including **object-oriented programming (OOP)** and **functional programming (FP)**.

---

## 🚀 Features

- **Create & Track Habits** – Define and monitor daily or weekly habits.
- **Analyze Progress** – View streaks, missed habits, and consistency stats.
- **Database Support** – Uses SQLite for data persistence.
- **Command-Line Interface (CLI)** – Interact with the application through the terminal.
- **Graphical User Interface (GUI)** – Built with Tkinter for an intuitive experience.
- **Automated Testing** – Includes unit tests for core functionalities.
- **Logging & Error Handling** – Captures errors and logs application activity.

---

## 📦 Installation

### **1. Clone the Repository**
Ensure you have **Git installed**, then run:

```sh
git clone https://github.com/YourUsername/habit-tracker.git
```

### **2. Create a Virtual Environment (Recommended)**
To **avoid dependency conflicts**, create and activate a virtual environment:

#### **Windows**
```sh
python -m venv venv
venv\Scripts\activate
```

#### **MacOS/Linux**
```sh
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## 🏰 Project Structure

```sh
habit-tracker/
├── src/
│   ├── app.py                # Main script for running the application
│   ├── database.py           # Handles SQLite database interactions
│   ├── habit.py              # Defines the Habit class and its methods
│   ├── analytics.py          # Functional programming logic for habit analysis
│   ├── gui.py                # Manages the Tkinter-based UI
│
├── tests/
│   ├── test_habit.py         # Unit tests for the Habit class
│   ├── test_database.py      # Tests for database queries
│
├── docs/                     # Documentation and diagrams
│   ├── user_flowchart.png     # User interaction flowchart
│   ├── component_diagram.png  # Module interaction diagram
│
├── config.json               # Stores configuration settings
├── setup.py                  # Helps with packaging and installation
├── requirements.txt          # Dependencies
├── LICENSE                   # License file
├── .gitignore                # Git ignore file
└── README.md                 # Project description
```

---

## 🛠 Usage

### **1. Running the Application**

After installation, start the habit tracker by running:

```sh
python src/app.py
```

### **2. CLI Commands**

| Command                | Description |
|------------------------|-------------|
| `add habit`           | Create a new habit |
| `check habit`         | Mark a habit as completed |
| `show habits`         | List all habits |
| `get stats`           | View habit statistics |
| `delete habit`        | Remove a habit |
| `exit`                | Close the application |

---

## ✅ Testing

This project includes **unit tests** to ensure functionality.

To run tests:

```sh
pytest
```

---

## 🤝 Contributing

Want to improve the project? Follow these steps:

1. **Fork** the repository.
2. **Clone** your fork:
   ```sh
   git clone https://github.com/YourUsername/habit-tracker.git
   ```
3. **Create a branch** for your changes:
   ```sh
   git checkout -b feature-branch-name
   ```
4. **Make modifications** and **commit**:
   ```sh
   git add .
   git commit -m "Added new feature"
   ```
5. **Push the branch**:
   ```sh
   git push origin feature-branch-name
   ```
6. **Submit a Pull Request** on GitHub.

---

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For any questions or suggestions, feel free to contact me at **siddiqui21shifa@gmail.com**.

---

