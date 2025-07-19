import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'habits.db')

def get_all_habits():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, periodicity, streak FROM habits')
    results = c.fetchall()
    conn.close()
    return results

def get_habits_by_periodicity(periodicity):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name FROM habits WHERE periodicity = ?', (periodicity,))
    results = c.fetchall()
    conn.close()
    return results

def get_longest_streak():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, MAX(streak) FROM habits')
    result = c.fetchone()
    conn.close()
    return result
