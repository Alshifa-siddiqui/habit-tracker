import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from datetime import datetime
import pytest
from habit import Habit
from habitDB import HabitDB
from analysis import (
    get_most_consistent_habits,
    get_most_struggled_habits,
    get_daily_habits,
    get_weekly_habits,
    calculate_completion_rate,
)
from Dates_Persistence import save_dates, delete_dates

class TestAnalysis:
    """ in this class we will test the analysis file
    pytest.fixtures:
         test_habit1 : Habit instance used for calling methods from habit and is used as a test habit
         db: HabitDB instance used to call methods from HabitDB
         clean_db: cleans the database after and before each test
         clean_pickle_files: deletes a pickle  file before and after each test
    methods:
         test_most_consistent_habit: testing if the program can correctly identify the most consistent habits
         test_most_struggling_habit: testing if the program can correctly identify the most struggling habits
         test_weekly_habits: testing if the program can correctly filter habits based on period and return  a list of weekly habits
         test_daily_habits: testing if the program can correctly filter habits based on period and return  a list of daily habits
         test_completion_rate: testing if the program can correctly calculate the completion rate """

    @pytest.fixture
    def test_habit(self):
        test_habit = Habit(name='zaidabuhijleh', period='daily', description='testing', streak=0, broken_count=0,
                           status='incomplete', created_at=datetime.now().date(), duration=100, day_week="day")
        return test_habit

    @pytest.fixture
    def test_habit1(self):
        test_habit1 = Habit(name='zaid', period='daily', description='testing', streak=0,
                            broken_count=0, status='incomplete', created_at=datetime.now().date(), duration=100,
                            day_week="day")
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


    @pytest.fixture(autouse=True)
    def clean_pickle_files1(self):
        delete_dates('zaidabuhijleh')
        yield
        delete_dates('zaidabuhijleh')



    def test_get_most_consistent_habits(self , db  , test_habit , test_habit1):
        """testing by creating 2 habits with a duration of 100 (one habit with streak of 5 and one with 0 since its broken)
        the result should be a list of names [test_habit1.name , test_habit] since we are sorting based on least broken streak count"""
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=100, day_week='day')
        db.create_habit(name=test_habit.name, period='daily', description='testing', duration=100, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        save_dates(test_habit.name, datetime(2024, 11, 1).date())
        save_dates(test_habit.name, datetime(2024, 11, 2).date())
        save_dates(test_habit.name, datetime(2024, 11, 3).date())
        save_dates(test_habit.name, datetime(2024, 11, 5).date())
        save_dates(test_habit.name, datetime(2024, 11, 6).date())
        db.update_status_streak(test_habit1.name)
        db.update_status_streak(test_habit.name)
        ex_outcome =[test_habit1.name ,test_habit.name ]
        result = get_most_consistent_habits(  db ,consistency=4)
        assert result == ex_outcome


    def test_get_most_struggled_habits(self , db  , test_habit , test_habit1):
        """testing by creating 2 habits with a duration of 100 (one habit with streak of 5 and one with 0 since its broken)
                the result should be a list of names [test_habit.name , test_habit1.name] since we are sorting based on largest broken streak count"""
        db.create_habit(name=test_habit.name, period='daily', description='testing', duration=100, day_week='day')
        db.create_habit(name=test_habit1.name, period='daily', description='fgds', duration=100, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        save_dates(test_habit.name, datetime(2024, 11, 1).date())
        save_dates(test_habit.name, datetime(2024, 11, 2).date())
        save_dates(test_habit.name, datetime(2024, 11, 3).date())
        save_dates(test_habit.name, datetime(2024, 11, 5).date())
        save_dates(test_habit.name, datetime(2024, 11, 6).date())
        db.update_status_streak( test_habit1.name)
        db.update_status_streak( test_habit.name)
        ex_outcome =[test_habit.name , test_habit1.name]
        result = get_most_struggled_habits(db,inconsistency=4)
        assert result == ex_outcome



    def test_weekly_habits(self, db, test_habit1, test_habit):
        """testing by creating 2 habits one daily and one weekly , it should return a list of daily habits names  """
        db.create_habit(name=test_habit.name, period='weekly', description='testing', duration=100, day_week='day')
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=100, day_week='day')
        result = get_weekly_habits(db)
        ex_outcome = [test_habit.name ]
        assert result == ex_outcome


    def test_daily_habits(self, db, test_habit1, test_habit):
        """testing by creating 2 habits one daily and one weekly , it should return a list of weekly habits names  """
        db.create_habit(name=test_habit.name, period='weekly', description='testing', duration=100, day_week='day')
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=100, day_week='day')
        result = get_daily_habits(db)
        ex_outcome = [test_habit1.name ]
        assert result == ex_outcome



    def test_completion_rate(self ,db , test_habit , test_habit1):
        """ testing if the method returns a correct  completion rate by calculating
         by creating 2 habits and setting one as completed and the other as incomplete
         the rate should be 50%"""
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=5, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        db.update_status_streak(test_habit1.name)
        rate1 = calculate_completion_rate(db)# 100%
        db.create_habit(name=test_habit.name, period='daily', description='testing', duration=100, day_week='day')
        rate2 = calculate_completion_rate(db)#50%
        assert rate2== '50.0%'
        assert rate1 != rate2