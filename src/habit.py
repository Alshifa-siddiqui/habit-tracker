from datetime import datetime, date
from Dates_Persistence import save_dates, load_dates
class Habit:
    """
    Represents a Class for Habit Management and Important Calculations.
    Methods:
        habit_is_done_today(): Appends the date when the user has completed their habit today.
        streak_calculations(): Calculates the streak of a habit and the broken streak count.
        longest_streak_run_for_a_given_habit(): Calculates the longest streak run for a given habit."""
    def __init__(self, name: str, period: str, description: str, streak: int, broken_count: int, status: str,created_at, duration: int = None, day_week: str = None):

        """
        Args:
            name (str): Name of the habit.
            period (str): Daily or weekly period for the habit.
            description (str): Description of the habit.
            streak (int): Number of consecutive dates the streak was completed.
            broken_count (int): Number of times the streak was broken.
            status (str): Status of the habit, e.g., "completed" or "incomplete".
            created_at (date): The date when the habit was created."""

        self.name = name
        self.period = period
        self.description = description
        self.streak = streak
        self.broken_count = broken_count
        self.status = status





    def habit_is_done_today(self, name: str ) -> None:
        """Append the date of the day if the user has completed their habit.
        Args:
            name (str): Name of the habit.
        Raises:
            ValueError: If the name is not provided.
            ValueError: If the date is duplicated.
        Returns:
            None: This method just appends the date of the day to `self.completed_dates`.
        Description:
            After validating that the name is provided and exists, the current date is appended to the list of completed dates,
            after checking that the date does not exist."""
        from habitDB import HabitDB
        db = HabitDB()

        if name is None:
            raise ValueError("Habit name is not provided ")
        if db.habit_exists(name):
             today = datetime.today().date()
             if today in load_dates(name):
                   raise ValueError("Date is duplicated")
             save_dates(name, date=today)


    def streak_calculations(self, name: str) -> tuple[int, int]:
        """Calculate the streak of a habit based on completed dates.
        Args:
            name (str): name of the habit
        Raises:
            ValueError : if name not provided
        Return:
            Two integers curr_streak and broken_count.
        Description of the method :
            We validate the name of the habit and after that we call to get the completed dates to do streak and broken count calculations
            this is done by looping over the date and checking if they are consecutive if they are we +1 to the streak and if the dates are not
            we set streak to 0 and broken count +1"""
        from habitDB import HabitDB
        db = HabitDB()

        if name is None:
            raise ValueError("name is not provided ")
        dates = sorted(load_dates(name))
        if not dates:
            return 0,0
        broken_count = 0
        curr_streak = 1 if len(dates) == 1 else 0
        for x in range(1, len(dates)):
            difference = (dates[x] - dates[x - 1]).days
            if db.get_period(name) == "daily":
                if difference == 1:
                    curr_streak += 1
                else:  # if dates are not consecutive set streak to zero and plus one to broken_count
                    broken_count += 1
                    curr_streak = 0
            elif db.get_period(name) == "weekly":
                if difference == 7:
                    curr_streak += 1
                else:
                    broken_count += 1
                    curr_streak = 0
        return curr_streak, broken_count


    def longest_run_streak_for_a_given_habit(self, name: str) -> int:
        """
        Calculate the longest streak run in a habit's history based on dates length.
        Args:
            name: Name of the habit (str).
        Raises:
            ValueError : if name not provided
        Return:
            Integer demonstrating the longest streak run of the habit in its history.
        Description of the method:
         after validating the name we check that the name matches one of the objects
         then we call load dates to get the completed dates and initialize streak history and consecutive dates list
         we set the gap 1 if the period daily and 7 if weekly and loop over the dates while the dates are consecutive
         append them to the list of consecutive dates the moment they are not consecutive append the length of consecutive dates to streak history
         and then start looping over the dates starting from the day the loop ended on , then return the max element in the list (longest streak run)
        """
        from habitDB import HabitDB
        db = HabitDB()

        if name is None:
            raise ValueError("name is not provided ")
        dates = sorted(load_dates(name))
        streak_history = []
        consecutive_dates = []
        gap = 1 if db.get_period(name) == 'daily' else 7  # Daily streak or weekly streak
        for x in range(1, len(dates)):
            if (dates[x] - dates[x - 1]).days == gap:
                consecutive_dates.append(dates[x])
            else:
                streak_history.append(len(consecutive_dates))
                consecutive_dates = [dates[x]]
        return max(streak_history) if streak_history else 0
        