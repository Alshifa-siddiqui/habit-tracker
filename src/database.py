import sqlite3
import shutil
import csv
import json
import os
from datetime import datetime, timedelta, date

# Explicit date adapter — the default one is deprecated in Python 3.12.
sqlite3.register_adapter(date, lambda d: d.isoformat())

class VitalisDB:
    def __init__(self, db_path="vitalis.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.migrate()
        self._ensure_indexes()

    def create_tables(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                avatar TEXT DEFAULT '🧑',
                age INTEGER DEFAULT 25,
                weight REAL DEFAULT 70,
                height REAL DEFAULT 170,
                medical_conditions TEXT DEFAULT '[]',
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                coins INTEGER DEFAULT 0,
                character_class TEXT DEFAULT 'Apprentice',
                hp INTEGER DEFAULT 100,
                strength INTEGER DEFAULT 10,
                endurance INTEGER DEFAULT 10,
                wisdom INTEGER DEFAULT 10,
                vitality INTEGER DEFAULT 10,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                name TEXT,
                frequency TEXT DEFAULT 'daily',
                category TEXT DEFAULT 'General',
                color TEXT DEFAULT '#7C3AED',
                difficulty INTEGER DEFAULT 1,
                goal_target INTEGER DEFAULT 30,
                habit_type TEXT DEFAULT 'custom',
                unit TEXT DEFAULT 'times',
                target_value REAL DEFAULT 1,
                completed_count INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                streak_freeze INTEGER DEFAULT 0,
                last_completed DATE DEFAULT NULL,
                reminder_time TEXT DEFAULT NULL,
                archived INTEGER DEFAULT 0,
                is_medical INTEGER DEFAULT 0,
                medical_category TEXT DEFAULT NULL,
                xp_reward INTEGER DEFAULT 10,
                stat_boost TEXT DEFAULT 'vitality',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS habit_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                user_id INTEGER DEFAULT 1,
                completed_date DATE,
                value REAL DEFAULT 1,
                note TEXT DEFAULT NULL,
                mood INTEGER DEFAULT NULL,
                energy INTEGER DEFAULT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            );
            CREATE TABLE IF NOT EXISTS mood_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                log_date DATE DEFAULT CURRENT_DATE,
                mood INTEGER,
                energy INTEGER,
                sleep_hours REAL DEFAULT NULL,
                stress INTEGER DEFAULT NULL,
                notes TEXT DEFAULT NULL
            );
            CREATE TABLE IF NOT EXISTS badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                badge_name TEXT,
                badge_icon TEXT DEFAULT '🏅',
                badge_desc TEXT DEFAULT '',
                earned_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS daily_challenge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                habit_id INTEGER,
                challenge_date DATE DEFAULT CURRENT_DATE,
                completed INTEGER DEFAULT 0,
                bonus_xp INTEGER DEFAULT 20
            );
            CREATE TABLE IF NOT EXISTS rpg_quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                quest_name TEXT,
                quest_desc TEXT,
                required_count INTEGER DEFAULT 7,
                progress INTEGER DEFAULT 0,
                completed INTEGER DEFAULT 0,
                reward_xp INTEGER DEFAULT 100,
                reward_coins INTEGER DEFAULT 50,
                expires_date DATE DEFAULT NULL
            );
            CREATE TABLE IF NOT EXISTS social_duels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                challenger_id INTEGER,
                opponent_name TEXT,
                habit_id INTEGER,
                start_date DATE DEFAULT CURRENT_DATE,
                end_date DATE,
                challenger_score INTEGER DEFAULT 0,
                opponent_score INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            );
            CREATE TABLE IF NOT EXISTS health_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE DEFAULT 1,
                blood_type TEXT DEFAULT NULL,
                bmi REAL DEFAULT NULL,
                resting_heart_rate INTEGER DEFAULT NULL,
                blood_pressure TEXT DEFAULT NULL,
                sleep_goal REAL DEFAULT 8,
                water_goal REAL DEFAULT 8,
                steps_goal INTEGER DEFAULT 10000,
                calorie_goal INTEGER DEFAULT 2000,
                doctor_notes TEXT DEFAULT NULL
            );
        """)
        self.cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'Vitalis User')")
        self.cursor.execute("INSERT OR IGNORE INTO health_profile (user_id) VALUES (1)")
        self.conn.commit()

    def migrate(self):
        cols = [
            "ALTER TABLE habits ADD COLUMN color TEXT DEFAULT '#7C3AED'",
            "ALTER TABLE habits ADD COLUMN category TEXT DEFAULT 'General'",
            "ALTER TABLE habits ADD COLUMN difficulty INTEGER DEFAULT 1",
            "ALTER TABLE habits ADD COLUMN goal_target INTEGER DEFAULT 30",
            "ALTER TABLE habits ADD COLUMN habit_type TEXT DEFAULT 'custom'",
            "ALTER TABLE habits ADD COLUMN unit TEXT DEFAULT 'times'",
            "ALTER TABLE habits ADD COLUMN target_value REAL DEFAULT 1",
            "ALTER TABLE habits ADD COLUMN streak_freeze INTEGER DEFAULT 0",
            "ALTER TABLE habits ADD COLUMN last_completed DATE DEFAULT NULL",
            "ALTER TABLE habits ADD COLUMN current_streak INTEGER DEFAULT 0",
            "ALTER TABLE habits ADD COLUMN longest_streak INTEGER DEFAULT 0",
            "ALTER TABLE habits ADD COLUMN reminder_time TEXT DEFAULT NULL",
            "ALTER TABLE habits ADD COLUMN archived INTEGER DEFAULT 0",
            "ALTER TABLE habits ADD COLUMN user_id INTEGER DEFAULT 1",
            "ALTER TABLE habits ADD COLUMN is_medical INTEGER DEFAULT 0",
            "ALTER TABLE habits ADD COLUMN medical_category TEXT DEFAULT NULL",
            "ALTER TABLE habits ADD COLUMN xp_reward INTEGER DEFAULT 10",
            "ALTER TABLE habits ADD COLUMN stat_boost TEXT DEFAULT 'vitality'",
            "ALTER TABLE habit_history ADD COLUMN note TEXT DEFAULT NULL",
            "ALTER TABLE habit_history ADD COLUMN user_id INTEGER DEFAULT 1",
            "ALTER TABLE habit_history ADD COLUMN value REAL DEFAULT 1",
            "ALTER TABLE habit_history ADD COLUMN mood INTEGER DEFAULT NULL",
            "ALTER TABLE habit_history ADD COLUMN energy INTEGER DEFAULT NULL",
        ]
        for sql in cols:
            try:
                self.cursor.execute(sql)
            except:
                pass
        self.conn.commit()

    def _ensure_indexes(self):
        # Remove any pre-existing duplicate check-ins so the unique index can be
        # created on legacy databases (keeps the earliest row per habit/day).
        self.cursor.execute("""
            DELETE FROM habit_history WHERE id NOT IN (
                SELECT MIN(id) FROM habit_history GROUP BY habit_id, completed_date
            )
        """)
        self.cursor.executescript("""
            CREATE INDEX IF NOT EXISTS idx_history_habit
                ON habit_history(habit_id);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_history_unique
                ON habit_history(habit_id, completed_date);
            CREATE INDEX IF NOT EXISTS idx_habits_user
                ON habits(user_id);
            CREATE INDEX IF NOT EXISTS idx_badges_user
                ON badges(user_id);
        """)
        self.conn.commit()

    def _row(self, r):
        return dict(r) if r else None

    # USERS
    def add_user(self, username, avatar='🧑'):
        try:
            self.cursor.execute("INSERT INTO users (username, avatar) VALUES (?,?)", (username, avatar))
            uid = self.cursor.lastrowid
            self.cursor.execute("INSERT OR IGNORE INTO health_profile (user_id) VALUES (?)", (uid,))
            self.conn.commit()
            return uid
        except sqlite3.IntegrityError:
            raise Exception(f"Username '{username}' already taken.")

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return [dict(r) for r in self.cursor.fetchall()]

    def get_user_by_id(self, uid):
        self.cursor.execute("SELECT * FROM users WHERE id=?", (uid,))
        return self._row(self.cursor.fetchone())

    def update_user(self, uid, **kwargs):
        for k, v in kwargs.items():
            self.cursor.execute(f"UPDATE users SET {k}=? WHERE id=?", (v, uid))
        self.conn.commit()

    def add_xp(self, user_id, xp):
        self.cursor.execute("UPDATE users SET xp=xp+?, coins=coins+? WHERE id=?", (xp, xp//5, user_id))
        self.cursor.execute("SELECT xp FROM users WHERE id=?", (user_id,))
        total = self.cursor.fetchone()[0]
        level = 1 + total // 100
        classes = {1:'Apprentice',5:'Seeker',10:'Warrior',20:'Champion',35:'Legend',50:'Vitalis Master'}
        cls = 'Apprentice'
        for req, name in sorted(classes.items()):
            if level >= req: cls = name
        self.cursor.execute("UPDATE users SET level=?, character_class=? WHERE id=?", (level, cls, user_id))
        self.conn.commit()

    def get_health_profile(self, user_id=1):
        self.cursor.execute("SELECT * FROM health_profile WHERE user_id=?", (user_id,))
        return self._row(self.cursor.fetchone()) or {}

    def update_health_profile(self, user_id, **kwargs):
        for k, v in kwargs.items():
            self.cursor.execute(f"UPDATE health_profile SET {k}=? WHERE user_id=?", (v, user_id))
        self.conn.commit()

    # HABITS
    def add_habit(self, name, frequency='daily', category='General', color='#7C3AED',
                  difficulty=1, goal_target=30, habit_type='custom', unit='times',
                  target_value=1, is_medical=0, medical_category=None,
                  reminder_time=None, stat_boost='vitality', xp_reward=10, user_id=1):
        self.cursor.execute("""
            INSERT INTO habits (user_id,name,frequency,category,color,difficulty,goal_target,
            habit_type,unit,target_value,is_medical,medical_category,reminder_time,stat_boost,xp_reward)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (user_id,name,frequency,category,color,difficulty,goal_target,
             habit_type,unit,target_value,is_medical,medical_category,reminder_time,stat_boost,xp_reward))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_habit(self, habit_id, **kwargs):
        for k, v in kwargs.items():
            self.cursor.execute(f"UPDATE habits SET {k}=? WHERE id=?", (v, habit_id))
        self.conn.commit()

    def delete_habit(self, habit_id):
        # Application-level cascade: remove dependent rows so deleting a habit
        # never leaves orphaned history/challenges/duels behind.
        self.cursor.execute("DELETE FROM habit_history WHERE habit_id=?", (habit_id,))
        self.cursor.execute("DELETE FROM daily_challenge WHERE habit_id=?", (habit_id,))
        self.cursor.execute("DELETE FROM social_duels WHERE habit_id=?", (habit_id,))
        self.cursor.execute("DELETE FROM habits WHERE id=?", (habit_id,))
        self.conn.commit()

    def archive_habit(self, habit_id):
        self.cursor.execute("UPDATE habits SET archived=1 WHERE id=?", (habit_id,))
        self.conn.commit()

    def unarchive_habit(self, habit_id):
        self.cursor.execute("UPDATE habits SET archived=0 WHERE id=?", (habit_id,))
        self.conn.commit()

    def get_habits(self, user_id=1, include_archived=False, category=None):
        q = "SELECT * FROM habits WHERE user_id=?"
        p = [user_id]
        if not include_archived:
            q += " AND archived=0"
        if category and category != "All":
            q += " AND category=?"
            p.append(category)
        q += " ORDER BY category, name"
        self.cursor.execute(q, p)
        habits = [dict(r) for r in self.cursor.fetchall()]
        for h in habits:
            h.update(self._compute_stats(h["id"], h.get("frequency")))
        return habits

    def get_habit_by_id(self, habit_id):
        self.cursor.execute("SELECT * FROM habits WHERE id=?", (habit_id,))
        row = self._row(self.cursor.fetchone())
        if row:
            row.update(self._compute_stats(habit_id, row.get("frequency")))
        return row

    # CHECK-IN
    # Allowed days between check-ins for the streak to continue, per frequency.
    _STREAK_GAP = {"daily": 1, "weekly": 7, "monthly": 31}

    @staticmethod
    def _streak_runs(dates, gap):
        """Given sorted distinct dates, return (longest_streak, current_streak).

        `current_streak` is the run ending at the most recent check-in, but only
        if that check-in is still within `gap` days of today (otherwise 0).
        """
        if not dates:
            return 0, 0
        longest = run = 1
        for i in range(1, len(dates)):
            run = run + 1 if 0 < (dates[i] - dates[i - 1]).days <= gap else 1
            longest = max(longest, run)
        current = 1
        for i in range(len(dates) - 1, 0, -1):
            if 0 < (dates[i] - dates[i - 1]).days <= gap:
                current += 1
            else:
                break
        if (date.today() - dates[-1]).days > gap:
            current = 0  # streak window has lapsed
        return longest, current

    def _compute_stats(self, habit_id, frequency):
        """Derive completion count and streaks from habit_history (source of
        truth), so the stored columns can never drift out of sync."""
        self.cursor.execute(
            "SELECT completed_date FROM habit_history WHERE habit_id=? ORDER BY completed_date",
            (habit_id,))
        dates = []
        for (raw,) in self.cursor.fetchall():
            try:
                dates.append(datetime.strptime(str(raw)[:10], "%Y-%m-%d").date())
            except (ValueError, TypeError):
                pass
        dates = sorted(set(dates))
        gap = self._STREAK_GAP.get((frequency or "daily").lower(), 1)
        longest, current = self._streak_runs(dates, gap)
        return {
            "completed_count": len(dates),
            "current_streak": current,
            "longest_streak": longest,
            "last_completed": dates[-1].isoformat() if dates else None,
        }

    def check_habit(self, habit_id, note=None, mood=None, energy=None, value=1, user_id=1):
        today = date.today()
        habit = self.get_habit_by_id(habit_id)
        if not habit:
            raise Exception("Habit not found.")
        self.cursor.execute(
            "SELECT id FROM habit_history WHERE habit_id=? AND completed_date=?", (habit_id, today))
        if self.cursor.fetchone():
            raise Exception("Already checked in today!")
        self.cursor.execute(
            "INSERT INTO habit_history (habit_id,user_id,completed_date,value,note,mood,energy) VALUES (?,?,?,?,?,?,?)",
            (habit_id, user_id, today, value, note, mood, energy))
        # completed_count / current_streak / longest_streak are derived from
        # habit_history on read (see _compute_stats), so nothing to update here.
        self.conn.commit()
        xp = habit['xp_reward'] * habit['difficulty']
        self.add_xp(user_id, xp)
        stat = habit.get('stat_boost', 'vitality')
        if stat in ['hp','strength','endurance','wisdom','vitality']:
            self.cursor.execute(f"UPDATE users SET {stat}=MIN({stat}+1,999) WHERE id=?", (user_id,))
            self.conn.commit()
        new_badges = self._check_badges(habit_id, user_id)
        return xp, new_badges

    def mark_habit_completed(self, habit_id, note=None, user_id=1):
        return self.check_habit(habit_id, note=note, user_id=user_id)

    def use_streak_freeze(self, habit_id):
        h = self.get_habit_by_id(habit_id)
        if h and h['streak_freeze'] > 0:
            self.cursor.execute("UPDATE habits SET streak_freeze=streak_freeze-1 WHERE id=?", (habit_id,))
            self.conn.commit()
            return True
        return False

    def add_streak_freeze(self, habit_id, n=1):
        self.cursor.execute("UPDATE habits SET streak_freeze=streak_freeze+? WHERE id=?", (n, habit_id))
        self.conn.commit()

    # HISTORY
    def get_habit_history(self, habit_id):
        self.cursor.execute(
            "SELECT * FROM habit_history WHERE habit_id=? ORDER BY completed_date ASC", (habit_id,))
        return [dict(r) for r in self.cursor.fetchall()]

    def get_history_dates(self, habit_id):
        self.cursor.execute(
            "SELECT completed_date FROM habit_history WHERE habit_id=? ORDER BY completed_date", (habit_id,))
        return [r[0] for r in self.cursor.fetchall()]

    # MOOD
    def log_mood(self, user_id, mood, energy, sleep_hours=None, stress=None, notes=None):
        today = date.today()
        self.cursor.execute("DELETE FROM mood_log WHERE user_id=? AND log_date=?", (user_id, today))
        self.cursor.execute(
            "INSERT INTO mood_log (user_id,log_date,mood,energy,sleep_hours,stress,notes) VALUES (?,?,?,?,?,?,?)",
            (user_id, today, mood, energy, sleep_hours, stress, notes))
        self.conn.commit()

    def get_mood_history(self, user_id, days=30):
        since = date.today() - timedelta(days=days)
        self.cursor.execute(
            "SELECT * FROM mood_log WHERE user_id=? AND log_date>=? ORDER BY log_date", (user_id, since))
        return [dict(r) for r in self.cursor.fetchall()]

    def get_today_mood(self, user_id):
        self.cursor.execute(
            "SELECT * FROM mood_log WHERE user_id=? AND log_date=?", (user_id, date.today()))
        return self._row(self.cursor.fetchone())

    # BADGES
    def _check_badges(self, habit_id, user_id):
        h = self.get_habit_by_id(habit_id)
        if not h: return []
        streak, count = h['current_streak'], h['completed_count']
        new_badges = []
        badge_map = [
            ("🔥","First Flame","Complete your first check-in", count>=1),
            ("⚡","Week Warrior","Maintain a 7-day streak", streak>=7),
            ("💎","Fortnight","Maintain a 14-day streak", streak>=14),
            ("🏆","Month Master","Maintain a 30-day streak", streak>=30),
            ("👑","Century","Complete 100 check-ins", count>=100),
            ("🌟","Consistent","Complete 50 check-ins", count>=50),
            ("🎯","Dedicated","Complete 30 check-ins", count>=30),
            ("💪","Iron Will","Maintain a 60-day streak", streak>=60),
            ("🦋","Transformed","Maintain a 90-day streak", streak>=90),
        ]
        for icon, name, desc, earned in badge_map:
            if earned:
                self.cursor.execute("SELECT id FROM badges WHERE user_id=? AND badge_name=?", (user_id, name))
                if not self.cursor.fetchone():
                    self.cursor.execute(
                        "INSERT INTO badges (user_id,badge_name,badge_icon,badge_desc) VALUES (?,?,?,?)",
                        (user_id, name, icon, desc))
                    new_badges.append(f"{icon} {name}")
        self.conn.commit()
        return new_badges

    def get_badges(self, user_id=1):
        self.cursor.execute("SELECT * FROM badges WHERE user_id=? ORDER BY earned_at DESC", (user_id,))
        return [dict(r) for r in self.cursor.fetchall()]

    # DAILY CHALLENGE
    def set_daily_challenge(self, habit_id, user_id=1):
        today = date.today()
        self.cursor.execute("DELETE FROM daily_challenge WHERE user_id=? AND challenge_date=?", (user_id, today))
        self.cursor.execute("INSERT INTO daily_challenge (user_id,habit_id,challenge_date) VALUES (?,?,?)", (user_id, habit_id, today))
        self.conn.commit()

    def get_daily_challenge(self, user_id=1):
        self.cursor.execute("""
            SELECT dc.*, h.name, h.category, h.color FROM daily_challenge dc
            JOIN habits h ON dc.habit_id=h.id
            WHERE dc.user_id=? AND dc.challenge_date=?""", (user_id, date.today()))
        return self._row(self.cursor.fetchone())

    def complete_daily_challenge(self, user_id=1):
        self.cursor.execute("UPDATE daily_challenge SET completed=1 WHERE user_id=? AND challenge_date=?", (user_id, date.today()))
        self.conn.commit()

    # QUESTS
    def add_quest(self, user_id, name, desc, required_count=7, reward_xp=100, reward_coins=50, days=7):
        expires = date.today() + timedelta(days=days)
        self.cursor.execute(
            "INSERT INTO rpg_quests (user_id,quest_name,quest_desc,required_count,reward_xp,reward_coins,expires_date) VALUES (?,?,?,?,?,?,?)",
            (user_id, name, desc, required_count, reward_xp, reward_coins, expires))
        self.conn.commit()

    def get_active_quests(self, user_id=1):
        self.cursor.execute(
            "SELECT * FROM rpg_quests WHERE user_id=? AND completed=0 AND (expires_date IS NULL OR expires_date>=?)",
            (user_id, date.today()))
        return [dict(r) for r in self.cursor.fetchall()]

    # SOCIAL DUELS
    def create_duel(self, user_id, opponent_name, habit_id, days=7):
        end = date.today() + timedelta(days=days)
        self.cursor.execute(
            "INSERT INTO social_duels (challenger_id,opponent_name,habit_id,end_date) VALUES (?,?,?,?)",
            (user_id, opponent_name, habit_id, end))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_active_duels(self, user_id=1):
        self.cursor.execute("""
            SELECT sd.*, h.name as habit_name FROM social_duels sd
            JOIN habits h ON sd.habit_id=h.id
            WHERE sd.challenger_id=? AND sd.status='active'""", (user_id,))
        return [dict(r) for r in self.cursor.fetchall()]

    # IMPORT/EXPORT/BACKUP
    def export_to_csv(self, filepath, user_id=1):
        habits = self.get_habits(user_id, include_archived=True)
        if not habits: raise Exception("No habits to export.")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=habits[0].keys())
            writer.writeheader()
            writer.writerows(habits)

    def import_from_csv(self, filepath, user_id=1):
        imported = 0
        with open(filepath, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    self.add_habit(name=row.get("name","Unnamed"),
                                   frequency=row.get("frequency","daily"),
                                   category=row.get("category","General"),
                                   user_id=user_id)
                    imported += 1
                except: pass
        return imported

    def backup_database(self, path):
        shutil.copy2(self.db_path, path)

    def restore_database(self, path):
        self.conn.close()
        shutil.copy2(path, self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
# Alias so gui.py import works
HabitDatabase = VitalisDB