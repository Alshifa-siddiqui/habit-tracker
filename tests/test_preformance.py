import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from datetime import datetime, timedelta
import pytest
from habit import Habit
from habitDB import HabitDB
from Dates_Persistence import save_dates, delete_dates

class TestPerformance:
    """ in this test I want to test if the Solution can handel large data not testing the speed of the execution
    pytest.fixtures:
         test_habit1 : Habit instance used for calling methods from habit and is used as a test habit
         db: HabitDB instance used to call methods from HabitDB
         clean_db: cleans the database after and before each test
         clean_pickle_files: deletes a pickle  file before and after each test
    methods:
    test_large_list_of_dates: test if the streak_calculations method can handel a large completed date list and can load the dates correctly
    test_create_large_amount_of_habits: test if the table in HabitDB can handel a large amount of habits created
    test_delete_large_number_of_habits: test if the program can handel   a mass deletion of habit at once
    test_fetch_from_large_db: test if the program can fetch data from the table correctly
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


    def test_large_list_of_dates(self , db  , test_habit1):
        """ testing if the program load data ( loading data is in the streak calculation method)  and the streak calculations method can correctly get the streak """
        db.create_habit(name=test_habit1.name, period='daily', description='testing', duration=10, day_week='day')
        dates= [(datetime(2024 ,1,1 ) +timedelta(days = i)).date() for i in range(500)]
        for date in dates:
            save_dates(test_habit1.name , date )
        curr_streak, broken_count = test_habit1.streak_calculations(test_habit1.name)
        assert curr_streak ==499
        assert broken_count ==0


    def test_create_large_amount_of_habits(self,db,test_habit1):
        """test if the DB can handel a large amount of creation """
        for h in range(1000):
            db.create_habit(name=f"{test_habit1.name}{h}", period='daily', description='testing', duration=10, day_week='day')
        all_habits = len(db.get_habits())
        assert all_habits ==1000

    def test_delete_large_number_of_habits(self, db, test_habit1):
        """ test if the DB can handel a mass deletion """
        for h in range(1000):
            db.create_habit(name=f"{test_habit1.name}{h}", period='daily', description='testing', duration=10, day_week='day')
        db.delete_all_habits()
        all_habits = len(db.get_habits())
        assert all_habits == 0


    def test_fetch_from_large_db(self,db , test_habit1):
        """ test if the user can handel a large creation of  habits and fetch data correctly """
        for h in range(1000):
            db.create_habit(name=f"{test_habit1.name}{h}", period='daily', description='testing', duration=10, day_week='day')
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