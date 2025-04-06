import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from datetime import datetime
import pytest

from habit import Habit
from habitDB import HabitDB
from Dates_Persistence import save_dates, delete_dates

class TestHabitDB:
    """Testing methods from HabitDB
     pytest.fixtures:
         test_habit1 : Habit instance used for calling methods from habit and is used as a test habit
         db: HabitDB instance used to call methods from HabitDB
         clean_db: cleans the database after and before each test
         clean_pickle_files: deletes a pickle  file before and after each test
     Methods:
         test_habit_exists: testing that the method that ensures no habits duplicated in the db works correctly
         test_create_habit: testing  the method that create  a habit create a habit and insert into the db
         test_delete_habit: testing the method that deletes a habit
         test_get_completed_habits: testing  the method that returns a completed habits list is working correctly
         test_get_incomplete_habits: testing the method that return a list of incomplete habits list working correctly
         test_get_streak: testing that the program fetches the streak correctly
         test_get_habits: testing the method that returns a all habits
         test_update_description: testing that this method updates the description correctly
         test_update_period: testing that this method updates the period correctly
         test_update_streak:testing that this method updates the streak correctly
         test_update_streak2:testing that this method when (streak ==duration) set the status to completed
         test_update_streak3: testing that this method updates the broken count in the DB
         test_delete_all_habits: testing that this method clears the db
         EDGE CASES:
            test_create_habit_that_exists: testing that the program raises an Error if the habit is duplicated
            test_delete_non_existing_habit: testing that the program raises an Error if the habit does not exists
            test_update_description_non_existing_habit: testing that the program raises an Error if the user tried to update a non existing habit
            test_update_period_of_non_existing_habit:testing that the program raises an Error if the user tried to update a non existing habit
            test_update_streak_status_non_existing_habit:testing that the program raises an Error if the user tried to update a non existing habit """

    @pytest.fixture
    def test_habit(self):
        test_habit = Habit(name='zaidabuhijleh', period='daily', description='testing', streak=0, broken_count=0, status='incomplete', created_at=datetime.now().date(), duration=100,day_week="day")
        return test_habit

    @pytest.fixture
    def test_habit1(self):
        test_habit1 = Habit(name='zaid', period='daily', description='testing', streak=0,
                            broken_count=0, status='incomplete', created_at=datetime.now().date(), duration=100 , day_week="day" )
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

    def test_habit_exists(self , db , test_habit1):
        """ testing that habit exists by creating a habit and then asserting that its in the DB"""
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=100, day_week='day')
        habit_exists = db.habit_exists(test_habit1.name)
        assert habit_exists == True
        assert db.habit_exists("zaid abu ") == False

    def test_create_habit(self,db):
        """Testing create habit method correctly insert habits into the db by comparing the number of habits before and after creation """
        name = 'zaid'
        habits = db.get_habits()
        habits_count = len(habits)
        db.create_habit(name=name, period='daily', description='testing', duration=100, day_week='day')
        habit_new = db.get_habits()
        habits_new_count = len(habit_new)
        assert habits_new_count == habits_count + 1
        assert name in [x[0] for x in habit_new]

    def test_delete_habit(self, test_habit1 , db ):
        """Testing that the method that deletes habits works correctly by comparing the number of habits after and before deletion  """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=100, day_week='day')
        db.delete_habit(test_habit1.name)
        after_deletion_habits = db.get_habits()
        assert test_habit1.name not in after_deletion_habits

    def test_get_completed_habits(self, test_habit1 ,db):
        """testing the get most completed habits by creating a habit and set it to completed and then compare the number of habits that are completed """
        initial = db.get_completed_habits()
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=5, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        db.update_status_streak(test_habit1.name)
        completed = db.get_completed_habits()
        assert test_habit1.name in completed
        assert len(completed) == len(initial) + 1

    def test_get_incomplete_habits(self, test_habit1 , db ):
        """testing the get most incomplete habits by creating a habit and compare the number of the in incomplete  habits after and before creation """
        initial = db.get_incomplete_habits()
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=100, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        db.update_status_streak( test_habit1.name)
        incomplete = db.get_incomplete_habits()
        assert test_habit1.name in [habit for habit in incomplete]
        assert len(incomplete) == len(initial) + 1



    def test_get_streak(self, test_habit1 , db ):
        """testing that the program fetches the streak from the db correctly after it gets updated in the db  """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=6, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        db.update_status_streak( test_habit1.name)
        ex_outcome = db.get_streak(test_habit1.name)
        assert ex_outcome == 5


    def test_get_habits(self,test_habit, test_habit1 , db ):
        """testing that the method(get_habits) fetch all habits correctly """
        initial = db.get_habits()
        db.create_habit(name=test_habit.name, period='daily', description='testing', duration=6, day_week='day')
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=6, day_week='day')
        habits = db.get_habits()
        assert len(habits) == len(initial) + 2
        assert test_habit.name in [name[0] for name in habits ]
        assert test_habit1.name in [name[0] for name in habits]

    def test_update_description(self, test_habit1 , db ):
        """testing that this method updates the description correctly """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=6, day_week='day')
        initial_desc = db.get_description(test_habit1.name)
        assert initial_desc == 'testing'
        db.update_description(test_habit1.name , 'new desc')
        new_desc = db.get_description(test_habit1.name)
        assert new_desc == 'new desc'
        assert new_desc != initial_desc





    def test_update_period(self, test_habit1 , db ):
        """testing that this method updates the period correctly """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=6, day_week='day')
        initial_period = db.get_period(test_habit1.name)
        db.update_period( test_habit1.name , 10 , 'day' )
        new_period = db.get_period(test_habit1.name)
        assert new_period == 'weekly'
        assert new_period != initial_period



    def test_update_streak(self, test_habit1 , db ):
        """testing that this method updates the streak correctly """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        db.update_status_streak(test_habit1.name)
        streak = db.get_streak(test_habit1.name)
        assert streak == 5

    def test_update_streak2(self, db,test_habit1  ):
        """testing that this method updates the streak correctly and set the habit as completed in the db """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 4).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        save_dates(test_habit1.name, datetime(2024, 11, 7).date())
        save_dates(test_habit1.name, datetime(2024, 11, 8).date())
        save_dates(test_habit1.name, datetime(2024, 11, 9).date())
        save_dates(test_habit1.name, datetime(2024, 11, 10).date())
        save_dates(test_habit1.name, datetime(2024, 11, 11).date())
        db.update_status_streak(test_habit1.name)
        streak = db.get_streak(test_habit1.name)
        completed_habit = db.get_completed_habits()
        assert streak == 10
        assert test_habit1.name in completed_habit

    def test_update_streak3(self, db,test_habit1  ):
        """test that the db gets updated if streak gets broken """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        save_dates(test_habit1.name, datetime(2024, 11, 1).date())
        save_dates(test_habit1.name, datetime(2024, 11, 2).date())
        save_dates(test_habit1.name, datetime(2024, 11, 3).date())
        save_dates(test_habit1.name, datetime(2024, 11, 5).date())
        save_dates(test_habit1.name, datetime(2024, 11, 6).date())
        db.update_status_streak(test_habit1.name)
        broken_count_post = db.get_broken_count(test_habit1.name)
        assert broken_count_post  == 1

    def test_delete_all_habits(self , db , test_habit1 , test_habit):
        """testing that this method clears the db """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        db.create_habit(name=test_habit.name, period='daily', description='testing', duration=10, day_week='day')
        pre_count = db.get_habits()
        db.delete_all_habits()
        post = db.get_habits()
        assert len(post) == 0
        assert len(pre_count) == len(post) +2


# test edge cases

    def test_create_habit_that_exists(self , db  ):
        """ensuring that the program rais ValueError if the habit exists"""
        name = 'omara dszaid '
        db.create_habit(name=name, period='daily', description='testing', duration=10, day_week='day')
        with pytest.raises(ValueError):
           db.create_habit(name=name, period='daily', description='testing', duration=10, day_week='day')

    def test_delete_non_existing_habit(self , db ):
        """Ensuring that the habit rais ValueError if the habit does not exists """
        name = 'omara dszaid '
        db.create_habit(name=name, period='daily', description='testing', duration=10, day_week='day')
        db.delete_habit(name)
        with pytest.raises(ValueError):
            db.delete_habit(name)

    def test_update_description_non_existing_habit(self , db , test_habit1 ):
        """Ensuring that the habit rais ValueError if the habit you want to update does not exist"""
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        db.delete_all_habits()
        with pytest.raises(ValueError):
            db.update_description(test_habit1.name , 'zaid ' )

    def test_update_period_of_non_existing_habit(self , db , test_habit1 ):
        """Ensuring that the habit rais ValueError if the habit you want to update does not exist"""
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        db.delete_all_habits()
        with pytest.raises(ValueError):
            db.update_period(test_habit1.name , 10 , 'day')

    def test_update_streak_status_non_existing_habit(self , db , test_habit1 ):
        """Ensuring that the habit rais ValueError if the habit you want to update does not exist"""
        db.create_habit(name=test_habit1.name , period='daily', description='testing', duration=10, day_week='day')
        db.delete_all_habits()
        with pytest.raises(ValueError):
            db.update_status_streak( test_habit1.name)