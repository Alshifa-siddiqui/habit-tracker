import matplotlib.pyplot as plt
from habit import Habit
from habitDB import HabitDB

"""
Analysis:

Functions:
1) db() 
    Returns an instance of HabitDB.

2)  get_most_consistent_habits()
   - Sorts habits based on the `broken_count` (the fewer, the more consistent).

3) get_most_struggled_habit()
   - Sorts habits based on the `broken_count` (the more, the less consistent).

4) get_daily_habits()
   - Filters habits based on the period (daily) and returns all habits with the daily period.

5) get_weekly_habits()
   - Filters habits based on the period (weekly) and returns all habits with the weekly period.

6) completion_rate()
   - Calculates the overall completion rate by dividing the number of completed habits by the total number of habits and then multiplying by 100.

7) report()
   - Provides a user with a report about their habits and progress.

8) visualization_performance_for_a_habit()
   - Creates a steam graph showing each habit's streak, allowing the user to visually see their performance."""


def db() -> HabitDB:
    """Initialize HabitDB """
    return HabitDB()


def get_most_consistent_habits(db: HabitDB, consistency: int) -> list:
    """Get most consistent habits sorted by the least amount of broken streak count.
    Args:
        db : HabitDB instance.
        consistency (int): the program is going to ask what in CLI  is considered as consistent and based on the user the programs acts
    Raises:
        ValueError: If no habits are found .
    Returns:
        A list of habit names that have broken streak counts less than or equal to the consistency"""
    habits = [name[0] for name in db.get_habits()]
    if not habits:
        raise ValueError("No habits found")
    if consistency is None:
        raise ValueError("consistency threshold not provided ")
    result = list(map(lambda name: (name, db.get_broken_count(name)), habits))
    sorted_result = sorted(result, key=lambda x: x[1])
    return [name for name, broken_count in sorted_result if broken_count <= consistency]


def get_most_struggled_habits(db: HabitDB, inconsistency: int) -> list:
    """Get most struggled habits sorted based on broken streak count
     Args:
         db :HabitDB instance
         inconsistency: (int)  the program is going to ask what in CLI  is considered as inconsistency and based on the user the programs acts
    Raises:
         ValueError : if no habit name provided
         ValeError : if no inconsistency provided
    Return:
          a list of habits sorted based on their broken streak count"""
    habits = [name[0] for name in db.get_habits()]
    if not habits:
        raise ValueError("No habits found")
    if inconsistency is None:
        raise ValueError("inconsistency threshold not provided ")
    result = list(map(lambda name: (name, db.get_broken_count(name)), habits))
    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)
    return [name for name, broken_count in sorted_result if broken_count <= inconsistency]


def get_daily_habits(db: HabitDB) -> list:
    """Filter habits by period (daily).
    Args:
        db : HabitDB instance
    Raises:
         None
    Returns:
         a list of habits with period of daily"""
    habits_data = db.get_habits()
    habits = [Habit(*habit) for habit in habits_data if Habit(*habit).period.strip() == 'daily']

    return list(map(lambda habit: habit.name, habits))


def get_weekly_habits(db: HabitDB) -> list:
    """Filter habits by period (weekly).
        Args:
            db : HabitDB instance
        Raises:
             None
        Returns:
             a list of habits with period of daily"""
    habits_data = db.get_habits()
    habit_instances = [Habit(*habit) for habit in habits_data if Habit(*habit).period.strip() == 'weekly']
    return list(map(lambda habit: habit.name, habit_instances))


def calculate_completion_rate(db: HabitDB) -> str:
    """Calculate the completion rate in percentage format
    Args:
        db : HabitDB instance
    Raises:
        ValueError : if there is no habits
    Return:
         a percentage of completion  """
    all_habits_number = len(db.get_habits())
    all_completed_habits = len(db.get_completed_habits())
    if all_habits_number == 0:
        raise ValueError("No habits found ")
    rate = all_completed_habits * 100 / all_habits_number
    return f"{rate}%"


def report(db: HabitDB, consistency: int, inconsistency: int) -> dict:
    """Generate a habit progress report"""
    return {
        "all habits": db.get_habits(),
        'most consistent habit': get_most_consistent_habits(db, consistency),
        'most struggled habit': get_most_struggled_habits(db, inconsistency),
        'daily habits': get_daily_habits(db),
        'weekly habits': get_weekly_habits(db),
        'over all completion rate ': calculate_completion_rate(db)}


def visualization_performance_for_a_habit(db: HabitDB):
    """visualize performance """
    names = [name[0] for name in db.get_habits()]
    streaks = list(map(lambda name: db.get_streak(name), names))
    plt.figure(figsize=(len(names) * 1.5, len(streaks) * 1.5))
    plt.stem(names, streaks)
    plt.xlabel(" habits")
    plt.ylabel(" streak")
    plt.title("User habits Performance")
    plt.tight_layout()
    plt.show()
    