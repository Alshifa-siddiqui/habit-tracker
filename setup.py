from setuptools import setup, find_packages

setup(
    name="habit_tracker",
    version="1.0.0",
    description="A Python Habit Tracker using OOP, Functional Programming, and SQLite",
    author="Alshifa Siddiqui",
    packages=find_packages(),
    install_requires=[
        "numpy~=1.26.4",
        "pandas~=2.1.4",
        "pytest~=7.4.4",
        "coverage~=7.4.3",
        "questionary~=2.0.1"
    ],
    entry_points={
        "console_scripts": [
            "habit-tracker=src.app:main"
        ]
    }
)
