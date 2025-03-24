import pytest
from Database import create_db, display_db, create_habit, remove_habit, complete_habit, display_periodicity, \
    display_highest_streak, display_highest_streak_periodicity  # Import all subroutines located in the Database.py file
import sqlite3
from datetime import datetime, timedelta  # Libraries to determine current date and times as well as differences in time
from main import Habits  # Import the Habits class from the main.py file


connection_test_db = sqlite3.connect("Habits.db")  # SQLite3 command to setup a connection to a defined DB (Habits.db)
cursor_test_db = connection_test_db.cursor()


def test_display_db():

    test_result = display_db()

    assert test_result[0].habit_name == "test_day", "expected test_day"
    assert test_result[1].habit_name == "test_week", "expected test_week"
    assert test_result[2].habit_name == "test_daily_streak", "expected test_daily_streak"
    assert test_result[3].habit_name == "test_weekly_streak", "expected test_weekly_streak"
    assert test_result[4].habit_name == "test_extra", "expected test_weekly_streak"


def test_create_habit():

    create_habit(Habits("reading", "daily"))
    create_habit(Habits("exercise", "weekly"))

    test_result = display_db()

    assert test_result[5].habit_name == "reading" and test_result[5].habit_periodicity == "daily", "expected reading"
    assert test_result[6].habit_name == "exercise" and test_result[6].habit_periodicity == "weekly", "expected test_week"


def test_remove_habit():

    remove_habit(Habits("reading", "daily"))

    test_result = display_db()
    assert test_result[5].habit_name == "exercise" and test_result[5].habit_periodicity == "weekly", "expected test_day"

    remove_habit(Habits("exercise", "weekly"))

    test_result = display_db()
    assert test_result[4].habit_name == "test_extra" and test_result[4].habit_periodicity == "daily", \
        "expected test_day"


def test_complete_habit():

    complete_habit(Habits("test_day", "daily"))

    test_result = display_db()
    assert (test_result[0].habit_name == "test_day" and test_result[0].habit_periodicity == "daily" and
            test_result[0].habit_complete == 1) and test_result[0].habit_streak == 1, "expected complete = 1"

    complete_habit(Habits("test_week", "weekly"))

    test_result = display_db()
    assert (test_result[1].habit_name == "test_week" and test_result[1].habit_periodicity == "weekly" and
            test_result[1].habit_complete == 1) and test_result[1].habit_streak == 2, "expected complete = 1"


def test_recompleted_habit():

    complete_habit(Habits("test_day", "daily"))

    test_result = display_db()
    assert (test_result[0].habit_name == "test_day" and test_result[0].habit_periodicity == "daily" and
            test_result[0].habit_complete == 1) and test_result[0].habit_streak == 1, "expected complete = 1"


def test_display_periodicity():

    test_result = display_periodicity("daily")
    assert test_result[0].habit_name == "test_day" and test_result[0].habit_periodicity == "daily", "expected period = daily"
    assert test_result[1].habit_name == "test_daily_streak" and test_result[1].habit_periodicity == "daily", "expected period = daily"

    test_result = display_periodicity("weekly")
    assert test_result[0].habit_name == "test_week" and test_result[0].habit_periodicity == "weekly", "expected period = weekly"
    assert test_result[1].habit_name == "test_weekly_streak" and test_result[1].habit_periodicity == "weekly", "expected period = weekly"


def test_longest_streak():

    test_result = display_highest_streak()
    assert test_result == "test_daily_streak"


def test_longest_streak_periodicity():

    test_result = display_highest_streak_periodicity("daily")
    assert test_result == "test_daily_streak"
    test_result = display_highest_streak_periodicity("weekly")
    assert test_result == "test_weekly_streak"
