import sqlite3
from datetime import datetime
from habit import Habit
from Dates_Persistence import delete_dates,create_file
connection = sqlite3.connect("habitDB.db")
cursor = connection.cursor()

cursor.execute("""
                  CREATE TABLE IF NOT EXISTS habits (
                      name TEXT PRIMARY KEY,
                      period TEXT CHECK (period IN ('daily', 'weekly')),
                      description TEXT,
                      streak INTEGER,
                      created_at INTEGER,
                      status TEXT CHECK (status IN ('completed', 'incomplete')),
                      broken_count INTEGER,
                      duration INTEGER ,
                      day_week TEXT)""")
connection.commit()


class HabitDB:

    """
    Class for Habit Management, Data Retrieval, and Storage.
    Methods:
    1) habit_exists(): Validates that the habit exists in the database to avoid redundant checks.
    2) create_habit(): Creates a habit and inserts it into the table. There are input values (handled in the CLI) and default parameters like streak, broken count, status, and created_at.
    3) delete_habit(): Deletes the habit after the user provides a name for the habit, checking if it exists in the table.
    4) get_completed_habits(): Fetches the habits that are completed.
    5) get_incomplete_habits(): Fetches the habits that are still in progress.
    6) get_streak(): Fetches the streak of a habit.
    7) get_broken_count(): Fetches the broken_count of a habit.
    8) longest_streak(): Fetches the longest streak of all running habits.
    9) get_description(): Fetches the description of a habit.
    10) get_period(): Fetches the period of a habit.
    11) get_habits(): Fetches all habits and all the parameters of each habit.
    12) delete_all_habits(): Clears the table.
    13) update_description(): Updates the description of a habit.
    14) update_period(): Updates the period of a habit.
    15) update_status_streak(): Updates the streak, broken_count, and status (if streak == duration).
    """

    def __init__(self):
        """initialize connection and a Habit instance """
        self.connection = sqlite3.connect("habitDB.db")
        self.habit= Habit(name='zaid',period='daily',description='testing',streak=0 ,broken_count=0 , status='incomplete' , created_at= datetime.now().date(), duration=100 , day_week="day" )



    def habit_exists(self, name: str) -> bool:# it's implemented to avoid redundancy
        """  a helper method to check if habit exists in the table
        Args:
             name(str) name of the habit
        Return
            bool: True if habit exists False  if not """
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM habits WHERE name = ?", (name,))
            return cursor.fetchone() is not None


    def create_habit(self, name: str, period: str, description: str, duration: int, day_week: str,created_at=datetime.now().date(), streak: int = 0, broken_count: int = 0, status: str = 'incomplete') -> None:
        """
        Creates a habit and inserts it into the table after validating its parameters.
        Args:
            name: Name of the habit.
            period: Period of the habit (daily/weekly).
            description: Description of the habit.
            duration: For how long you want this habit to last.
            day_week: Unit of measuring duration (e.g., duration=10, 10 days or 10 weeks).
            created_at: Date the habit was created.
            streak: Streak of the habit.
            broken_count: How many times the streak was broken.
            status: (completed, incomplete).
        Raises:
            ValueError: If the habit does not exist.
            ValueError: If the name is None.
            ValueError: If the period is invalid.
            ValueError: If the description is None.
            ValueError: If the duration is None.
            ValueError: If the day_week is None.
            ValueError: If the day_week is invalid.
        Description of method:
            After we validate the parameters of the habit and check that the habit does not exist in the table,
            we initialize the connection and insert those parameters into the table.
           There are some parameters that are default for a fresh habit, like streak, broken count, status, and created_at,
           while others will be provided as input in the CLI."""
        if name is None:
            raise ValueError("Name is invalid ")
        if period is None:
            raise ValueError("Habit period (daily/weekly) is required")
        if period not in ('daily', 'weekly'):
            raise ValueError("Invalid period, must be 'daily' or 'weekly'")
        if description is None:
            raise ValueError("Habit description is required")
        if duration is None:
            raise ValueError("Habit duration is required")
        if day_week is None:
            raise ValueError("Day/Week unit is required")
        if day_week not in ('day', 'week'):
            raise ValueError("Invalid day/week value")
        if self.habit_exists(name):
            raise ValueError("Habit already exists")
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO habits(name , period , description , streak,created_at , status , broken_count,duration, day_week) VALUES (?,?,?,?,?,?,?,?,?)""",
                (name, period, description, streak, created_at, status, broken_count, duration, day_week))
            connection.commit()
            create_file(name)



    def delete_habit(self, name: str) -> None:
        """ Delete a habit from the table
        Args:
             name : name of the habit
        Raises :
           ValueError if the name of the habit does not exist
           return : the function return nothing it deletes the habit

        Description of method:
          firstly we create a connection and Initialize the cursor
          then we validate the name args that its provided and check if the habit exists
          then we delete the habit based on name """
        with self.connection as connection:
            cursor = connection.cursor()
            if name is None:
                raise ValueError("Name not Provided  ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found in the database  ")
            cursor.execute("""DELETE FROM habits WHERE name = ?""", (name,))
            connection.commit()
            delete_dates(name)




    def get_completed_habits(self) -> list[str]:
        """ fetches habits with status of completed
         Args:
             None
         Raises :
             None
         Return:
              list of names of the completed habits """
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * FROM habits WHERE status = ?""", ("completed",))
            done_ = cursor.fetchall()
            return [name[0] for name in done_] if done_ else []

    def get_incomplete_habits(self) -> list[str]:
        """ fetch all habits with status of incomplete"""
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * FROM habits WHERE status = ?""", ("incomplete",))
            undone_ = cursor.fetchall()
            return [name[0] for name in undone_] if undone_ else []

    def get_streak(self, name: str) -> int:
        """ fetches the streak of the habit after it checks if the name of the habit exists
        Args:
            name of the habit
        Raises:
           ValueError if the name of the habit does not exist
        Return:
             int demonstrating the  streak count of a habit"""
        with self.connection as connection:
            cursor = connection.cursor()
            if name is  None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found in the table ")
            cursor.execute("""SELECT streak FROM habits WHERE name = ?""", (name,))
            streak = cursor.fetchone()
            return streak[0] if streak else None


    def get_broken_count(self, name: str) -> int:
        """fetches the broken count of a habit based on the name
        Arg:
           name(str): of the habit
        Raises :
            ValueError if the name of the habit does not exist
            ValueError if the Habit  does not exist
        Return:
             int demonstrating the broken streak count of a habit """
        with self.connection as connection:
            cursor = connection.cursor()
            if name is  None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found ")
            cursor.execute("""SELECT broken_count FROM habits WHERE name = ?""", (name,))
            broken_count = cursor.fetchone()
            return broken_count[0] if broken_count else None


    def longest_streak(self) -> int:
        """ fetch the longest streak of running habit
         Args:
             None
         Raises :
            None
         Return:
              int (max streak of running habits ) """
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT MAX(streak) FROM habits WHERE status = 'incomplete' """)
            streaks = cursor.fetchall()
            return streaks[0] if streaks else []

    def get_description(self, name: str) -> str:
        """ fetch the description of a habit
        Args:
            name of the habit
        Raises:
            ValueError if the habit does not exist
        Return :
         (str) description of the habit """
        with self.connection as connection:
            cursor = connection.cursor()
            if name is  None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found ")
            cursor.execute(""" SELECT description FROM habits WHERE name = ? """, (name,))
            description = cursor.fetchone()
            return description[0] if description else None

    def get_period(self, name: str) -> str:
        """ fetch the description of a habit
            Args:
                 name of the habit
            Raises:
                 ValueError if the habit does not exist
            Return :
                 (str) description of the habit """
        with self.connection as connection:
            cursor = connection.cursor()
            if name is  None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found ")
            cursor.execute(""" SELECT period FROM habits""")
            period = cursor.fetchone()
            return period[0] if period else None

    def get_habits(self) -> list[tuple]:
        """ fetches all habits and all info about the habit
           Args:
               None
           Raises:
               None
            Return:
                a list of tuples of all habits and its parameters"""
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * FROM habits""")
            habits = cursor.fetchall()
            return habits if habits else []



    def delete_all_habits(self) -> None:
        """deletes all habits and records from Table """
        with self.connection as connection:
            cursor = connection.cursor()
            for habit in [habit[0] for habit in self.get_habits()]: # deletes the dates before deleting habit records
                delete_dates(habit)
            cursor.execute("DELETE FROM habits")
            connection.commit()


    def update_description(self, name: str,new_desc: str) -> None:
        """ Update the description of a habit
        Args:

           new_desc : the new description
           name : name of the habit
        Raises:
            ValueError if the name is not provided
            ValueError if the new description is not provided
            ValueError if the habit does not exist
        Return :
           returns nothing only updates value in the table"""
        with self.connection as connection:
            cursor = connection.cursor()
            if name is None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found ")
            if new_desc is None:
                raise ValueError("New description is invalid")
            cursor.execute("UPDATE habits SET description = ? WHERE name = ?", (new_desc, name))
            connection.commit()



    def update_period(self,  name:str, duration: int, day_week: str ) -> None:
        """ update the period of a habit
        Args :

           name: of th habit
           duration: the duration of the habit
           day_week: unit of measuring the duration in days or weeks
        Raises:
            ValueError if the name is not provided
            ValueError if the duration is not provided
            ValueError if the day_week is not provided
            ValueError if the habit does not exist

        Return :
           returns nothing but update the values in the table and attribute

        Description of the method :
            after validating the name duration and day_week and if the habit exists
            we fetch the period of the habit if it was daily we change it to weekly and ask
            about the new duration of the habit and day_week
            and same goes for if the habit was weekly """
        with self.connection as connection:
            cursor = connection.cursor()
            if name is None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found ")
            if duration is None:
                raise ValueError("duration cant be None please provide a duration")
            if day_week is None:
                raise ValueError("day_week cant be None please provide a day_week")
            cursor.execute(""" SELECT period FROM habits WHERE name= ? """, (name,))
            period = cursor.fetchone()
            period_ = period[0] if period else None
            if period_ == "daily":
                cursor.execute("""UPDATE habits SET period = 'weekly', duration =? ,day_week = ? WHERE name = ? """, (day_week, duration, name))
                connection.commit()
            elif period_ == "weekly":
                cursor.execute("""UPDATE habits SET period = 'daily', duration =?, day_week = ? WHERE name = ? """,(duration, day_week, name))
                connection.commit()


    def update_status_streak(self,  name: str) -> None:
        """ Update the streak , broken_count and possibly the status

        Arg:
          name of the habit
        Raises:
            ValueError if the habit does not exist
            ValueError if the name is not provided

        Return :
          return nothing just updates the streak in the table

        Description of the method:
            after validating the name and if it exists
            we fetch the duration and call the streak calculator function
            as long as the streak is less than the duration update the table
            column streak with this streak if streak == duration tha habit is completed
            and if the broken count is more than the original broken count set streak to 0 and assign the new broken count """
        with self.connection as connection:
            cursor = connection.cursor()
            curr_streak, broken_count = self.habit.streak_calculations(name)
            if name is None:
                raise ValueError("Name not Provided ")
            if self.habit_exists(name) is False:
                raise ValueError("Habit not found ")
            cursor.execute(""" SELECT duration FROM habits WHERE name = ?""", (name,))
            duration_ = cursor.fetchone()
            duration = duration_[0]
            if duration:
                if curr_streak < duration:
                    cursor.execute(""" UPDATE habits SET streak = ? WHERE name = ? """, (curr_streak, name))
                    connection.commit()
                elif curr_streak == duration:
                    cursor.execute(""" UPDATE habits SET status = ?  ,streak = ? WHERE name = ? """, ("completed",int(duration), name))
                    connection.commit()
                if broken_count > self.get_broken_count(name):
                    cursor.execute(""" UPDATE habits SET streak = 0 ,broken_count= ? WHERE name = ?""", (broken_count, name))
                    connection.commit()