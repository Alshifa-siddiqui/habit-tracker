from setuptools import setup, find_packages

setup(
    name="habit_tracker",
    version="1.0.0",
    description="Vitalis — a Python Habit Tracker using OOP, Functional Programming, and SQLite",
    author="Alshifa Siddiqui",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "numpy~=1.26.4",
        "matplotlib~=3.9.2",
    ],
    extras_require={
        "dev": ["pytest~=7.4.4", "coverage~=7.4.3"],
    },
    # The app's modules import each other as top-level modules (e.g.
    # `from database import ...`), so it is run directly rather than via a
    # console-script entry point:  python src/app.py
)
