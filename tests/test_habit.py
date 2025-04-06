import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from datetime import datetime
import pytest
from habit import Habit
from habitDB import HabitDB
from Dates_Persistence import save_dates, load_dates, delete_dates

class TestHabit:
    """testing Habit class
     pytest.fixtures:
         test_habit1 : Habit instance used for calling methods from habit and is used as a test habit
         db: HabitDB instance used to call methods from HabitDB
         clean_db: cleans the database after and before each test
         clean_pickle_files: deletes a pickle  file before and after each test
     methods :
         test_habit_is_done_today: testing if the method works correctly by calling it and asserting  that the dates is in the list of completed dates
         test_streak_calculation: testing if the method correctly calculate  the streak for daily habits
         test_streak_cal_for_broken_count: testing if the method correctly calculate the broken count for a daily habit
         test_streak_cal_for_weekly_habits_broken_count: testing if the method correctly calculate the broken count for a weekly habit
         test_streak_for_weekly_habits:  testing if the method correctly calculate  the streak for weekly habits
         test_longest_run_streak_for_a_given_habit : testing if the method correctly calculate the longest streak run of a habit
         EDGE CASES:
             test_streak_cal_for_empty_dates_list: testing the streak_calculations method returns 0 since we dont have completed dates
             test_streak_when_only_1_dates:  testing the streak_calculations method returns 1 since we only have one completed date
             test_duplicated_dates: test if the program correctly raise a ValueError if the dates are duplicated 1
     """
    @pytest.fixture
    def test_habit1(self):
        test_habit1 = Habit(name='zaid', period='daily', description='testing', streak=0, broken_count=0,
                            status='incomplete', created_at=datetime.now().date(), duration=100, day_week="day")
        return test_habit1

    @pytest.fixture
    def db(self):
        return HabitDB()

    @pytest.fixture(autouse=True)
    def clean_db(self, db):
        db.delete_all_habits()
        yield
        db.delete_all_habits()

    @pytest.fixture(autouse=True)
    def clean_pickle_files(self):
        delete_dates('zaid')
        yield
        delete_dates('zaid')

    def test_habit_is_done_today(self, db, test_habit1):
        """ testing the habit is done today by asserting the date in the completed dates list """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        test_habit1.habit_is_done_today(test_habit1.name)
        assert datetime.now().date() in load_dates(test_habit1.name)

    def test_streak_calculation(self, test_habit1, db):
        """testing streak_calculations for daily habits by giving it consecutive dates  """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        curr_streak, broken_count = test_habit1.streak_calculations(test_habit1.name)
        assert curr_streak == 5
        assert broken_count == 0

    def test_streak_cal_for_broken_count(self, test_habit1, db):
        """testing streak_calculations for daily habits by giving it none-consecutive dates  """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        curr_streak, broken_count = test_habit1.streak_calculations(test_habit1.name)
        assert broken_count == 2

    def test_streak_for_weekly_habits(self, test_habit1, db):
        """testing streak_calculations for weekly habits by giving it consecutive dates  """
        db.create_habit(name=test_habit1.name, period='weekly', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 10, 1).date())
        save_dates(test_habit1.name, datetime(2024, 10, 8).date())
        save_dates(test_habit1.name, datetime(2024, 10, 15).date())
        curr_streak, broken_count = test_habit1.streak_calculations(test_habit1.name)
        assert curr_streak == 2

    def test_streak_cal_for_weekly_habits_broken_count(self, test_habit1, db):
        """testing streak_calculations for weekly habits by giving it none-consecutive dates  """
        db.create_habit(name=test_habit1.name, period='weekly', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 15).date())
        curr_streak, broken_count =test_habit1.streak_calculations(test_habit1.name)
        assert broken_count == 1


    def test_longest_run_streak_for_a_given_habit(self, test_habit1, db):
        """test longest streak run method by creating a habit and then save 15 days as completed dates the first 8 days are consecutive then
        they get broken the method should return 7 """
        db.create_habit(name=test_habit1.name, period=test_habit1.period, description=test_habit1.description,duration=100, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 10, 1).date())
        save_dates(test_habit1.name, datetime(2024, 10, 2).date())
        save_dates(test_habit1.name, datetime(2024, 10, 3).date())
        save_dates(test_habit1.name, datetime(2024, 10, 4).date())
        save_dates(test_habit1.name, datetime(2024, 10, 5).date())
        save_dates(test_habit1.name, datetime(2024, 10, 6).date())
        save_dates(test_habit1.name, datetime(2024, 10, 7).date())
        save_dates(test_habit1.name, datetime(2024, 10, 8).date())
        save_dates(test_habit1.name, datetime(2024, 10, 10).date())
        save_dates(test_habit1.name, datetime(2024, 10, 11).date())
        save_dates(test_habit1.name, datetime(2024, 10, 12).date())
        save_dates(test_habit1.name, datetime(2024, 10, 13).date())
        save_dates(test_habit1.name, datetime(2024, 10, 15).date())
        ex_outcome = test_habit1.longest_run_streak_for_a_given_habit(test_habit1.name)
        assert ex_outcome == 7

# test edge cases : (empty dates, 1 date only, duplication   )
    def test_streak_cal_for_empty_dates_list(self, test_habit1, db):
        """test streak calculations with an empty completed dates list  """
        db.create_habit(name=test_habit1.name, period=test_habit1.period, description=test_habit1.description,duration=100, day_week='day')
        delete_dates(test_habit1.name)
        ex_outcome = 0
        curr_streak, broken_count = test_habit1.streak_calculations(test_habit1.name)
        assert curr_streak == ex_outcome

    def test_streak_when_only_1_dates(self, test_habit1, db):
        """test streak calculations with 1 completed date   """
        db.create_habit(name=test_habit1.name, period=test_habit1.period, description=test_habit1.description,duration=100, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 10, 1))
        ex_outcome = 1
        curr_streak, broken_count = test_habit1.streak_calculations(test_habit1.name)
        assert curr_streak == ex_outcome


    def test_duplicated_dates(self , db , test_habit1):
        """ensuring that if the dates are duplicated that it raises an Error """
        db.create_habit(name=test_habit1.name, period=test_habit1.period, description=test_habit1.description,
                        duration=100, day_week='day')
        test_habit1.habit_is_done_today(test_habit1.name )
        with pytest.raises(ValueError):
            test_habit1.habit_is_done_today(test_habit1.name )
            