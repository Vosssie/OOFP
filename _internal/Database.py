import sqlite3  # Library used to create, define and manipulate databases using SQL
import os   # Library to execute commands that can clear the CLI for a clean interface
from datetime import datetime, timedelta  # Libraries to determine current date and times as well as differences in time
from main import Habits  # Import the Habits class from the main.py file


connection_db = sqlite3.connect('Habits.db')    # SQLite3 command to setup a connection to a defined DB (Habits.db)
cursor_db = connection_db.cursor()      # SQLite3 command to point a cursor to the BD connection


def create_db():
    """
    Function that:
        - Checks if a DB called Habits exits
            - If not → Creates one
            - If yes:
                - Checks and updates pastComplete field to reset Completion criteria for a habit
                - Reads the DB row by row
                - Passes each row as an instance into the class habits

    :return: A list of instances for the class Habits
    """

    # Database is created if it does not exist
    cursor_db.execute(
        "CREATE TABLE IF NOT EXISTS Habits(name TEXT, periodicity TEXT, number INTEGER, start DATE,"
        " completion INTEGER, pastComplete DATE, streak INTEGER)")
    connection_db.commit()

    empty_db = cursor_db.execute("SELECT COUNT(name) FROM Habits")

    if empty_db.fetchone()[0] == 0:
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.replace(microsecond=0)
        new_habit_daily_list = ["test_day", "daily", 1, yesterday, 0, yesterday, 1]

        week_ago = (today - timedelta(days=7)).replace(microsecond=0)
        weeks_ago = (today - timedelta(days=28)).replace(microsecond=0)
        less_week_ago = (today - timedelta(days=5)).replace(microsecond=0)
        new_habit_weekly_list = ["test_week", "weekly", 2, week_ago, 0, less_week_ago, 1]

        new_habit_daily_streak = ["test_daily_streak", "daily", 3, week_ago, 1, yesterday, 7]
        new_habit_weekly_streak = ["test_weekly_streak", "weekly", 4, weeks_ago, 1, yesterday, 4]
        new_habit_daily = ["test_extra", "daily", 5, yesterday, 0, yesterday, 1]

        cursor_db.execute("INSERT INTO Habits VALUES (?, ?, ?, ?, ?, ?, ?)", new_habit_daily_list)
        cursor_db.execute("INSERT INTO Habits VALUES (?, ?, ?, ?, ?, ?, ?)", new_habit_weekly_list)
        cursor_db.execute("INSERT INTO Habits VALUES (?, ?, ?, ?, ?, ?, ?)", new_habit_daily_streak)
        cursor_db.execute("INSERT INTO Habits VALUES (?, ?, ?, ?, ?, ?, ?)", new_habit_weekly_streak)
        cursor_db.execute("INSERT INTO Habits VALUES (?, ?, ?, ?, ?, ?, ?)", new_habit_daily)
        connection_db.commit()

    # Section of code to reset the Completion variable for each instance of habit if it is a new day
    cursor_db.execute("SELECT pastComplete FROM Habits")
    returned = cursor_db.fetchall()  # All habits must be fetched to check for updates
    day = timedelta(days=1)  # One day is used as a habit can be completed the next day for a DAILY or WEEKLY habit
    for row in returned:
        row = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")  # Strip the millisecond data from the date
        rows = datetime.date(row)  # Leave only the date as a habit can be completed at different times throughout a day
        if (datetime.now().date() - rows) >= day:  # Check if more than a day has passed since last complete
            print("YES")
            cursor_db.execute("UPDATE Habits SET completion = 0 WHERE pastComplete = ?", [row])  # Rest Completion
            connection_db.commit()
    cursor_db.execute("SELECT * FROM Habits")
    returned = cursor_db.fetchall()
    row_habits = []
    for row in returned:  # Pass each row as an instance into the Habits class
        row_habits.append(
            Habits(habit_name=row[0], habit_periodicity=row[1], habit_number=row[2], habit_start_date=row[3],
                   habit_complete=row[4], habit_last_complete=row[5], habit_streak=row[6]))

    return row_habits  # Return the list of habits


def display_db():
    """
    Function to display all active habits and the relevant info for each habit

    :return: Returns a list of all habits as instances of the Habits class
    """

    os.system('cls' if os.name == 'nt' else 'clear')  # OS command to clear the console for ease of reading
    print(
        f"{'Name':<{20}} {'Period':<{10}} {'Number':<{10}} {'Start Date':<{25}} {'Complete':<{10}} "
        f"{'Last Completed':<{25}} {'Streak':<{10}}")  # Heading format to read the habit data easily
    # Seperator string
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cursor_db.execute("SELECT * FROM Habits")
    returned = cursor_db.fetchall()
    all_habits = []
    for row in returned:
        all_habits.append(
            Habits(habit_name=row[0], habit_periodicity=row[1], habit_number=row[2], habit_start_date=row[3],
                   habit_complete=row[4], habit_last_complete=row[5], habit_streak=row[6]))
    for habit in all_habits:
        print(habit)  # To display all instances of the habit class read from the DB
    return all_habits


def display_periodicity(periodicity):
    """
    Procedure to display ALL habits of a particular periodicity
    :param periodicity: User defined periodicity to search for
    :return: N/A : Only displays the relevant DB rows
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        f"{'Name':<{20}} {'Period':<{10}} {'Number':<{10}} {'Start Date':<{25}} {'Complete':<{10}} "
        f"{'Last Completed':<{25}} {'Streak':<{10}}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cursor_db.execute("SELECT * FROM Habits WHERE periodicity = ?", [periodicity])  # Search for particular period
    returned = cursor_db.fetchall()
    all_habits = []
    for row in returned:
        all_habits.append(
            Habits(habit_name=row[0], habit_periodicity=row[1], habit_number=row[2], habit_start_date=row[3],
                   habit_complete=row[4], habit_last_complete=row[5], habit_streak=row[6]))
    for habit in all_habits:
        print(habit)  # Display all applicable habits as an instance of the habits class for the formatting
    return all_habits


def display_highest_streak():
    """
    Procedure to display the highest streak of any active habit regardless of periodicity
    :return: N/A : Displays the name of the habit and the current streak. Habit class __repro__ not required for format
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    cursor_db.execute("SELECT name, Max(streak) FROM Habits WHERE streak = (SELECT MAX(streak) FROM Habits)")
    longest_streak_habit = cursor_db.fetchone()[0]  # To fetch the return tuple as single value [0]
    cursor_db.execute("SELECT Max(streak) FROM Habits")  # MAX function used to get the largest value
    longest_streak = cursor_db.fetchone()[0]
    print("The habit with the total longest streak is: ", longest_streak_habit, "with", longest_streak, "completions")
    return longest_streak_habit


def display_highest_streak_periodicity(periodicity):
    """
    Procedure to display the habit with the longest streak for a GIVEN periodicity
    :param periodicity: User defined period to search
    :return: N/A : Simply displays the habit name and streak
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    cursor_db.execute(
        "SELECT name FROM Habits WHERE periodicity = ? ORDER BY streak DESC",
        [periodicity])
    longest_streak_habit = cursor_db.fetchone()[0]  # Only a single value needed NOT tuple
    cursor_db.execute("SELECT Max(streak) FROM Habits WHERE periodicity = ?", [periodicity])
    longest_streak = cursor_db.fetchone()[0]
    print("The", periodicity, "with the longest streak is: ", longest_streak_habit, "with", longest_streak,
          "completions")
    return longest_streak_habit


def create_habit(habit: Habits):
    """
    Procedure to append a new user defined habit to the Habits database.
    Name and periodicity are provided
    Default info:
        - Habit number → Determined through count increment
        - Start date → Determined as the current date and time with microseconds stripped
        - Completion → Set to default as the habit could not have been completed yet
        - PastCompletion → Set to current date and time in order to determine streak data
        - Streak  → Defaulted to zero as the habit has not been completed yet

    :param habit: Habits class instance passed such that the user defined name and periodicity can be used
    :return: N/A : Simply adds the habit and default habit information to the database
    """

    cursor_db.execute("SELECT COUNT(*) FROM Habits")  # Determine the number of active habits in the database
    count = cursor_db.fetchone()[0]  # Return single data
    new_habit_number = count + 1  # Increment this count such that the new habit has the correct number

    new_habit_list = [habit.habit_name, habit.habit_periodicity, new_habit_number,
                      datetime.now().replace(microsecond=0), 0, datetime.now().replace(microsecond=0), 0]

    cursor_db.execute("INSERT INTO Habits VALUES (?, ?, ?, ?, ?, ?, ?)", new_habit_list)
    connection_db.commit()  # Commit changes to the database
    print("Habit successfully created")


def remove_habit(habit: Habits):
    """
    Deletes an active habit from the Database
    :param habit: Receives a Habits class instance such that all habit relevant habit info can be accessed
    :return: N/A : Simply removes the habit from the DB. Display-habits can be used to refresh list of active habits
    """

    cursor_db.execute("SELECT number FROM Habits WHERE name = ? AND periodicity = ?",
                      [habit.habit_name, habit.habit_periodicity])
    row = cursor_db.fetchone()

    if row is None:
        print("No such Habit and Period combination")
        return
    row = row[0]
    cursor_db.execute("UPDATE Habits SET number = number - 1 WHERE number > ?", [row])  # Update habit numbers
    cursor_db.execute("DELETE FROM Habits WHERE name = ? AND periodicity = ?",
                      [habit.habit_name, habit.habit_periodicity])  # Removal of habit
    connection_db.commit()  # Commit changes to DB
    print("Habit successfully removed")


def complete_habit(habit: Habits):
    """
    Procedure to mark an active habit as completed for the associated time period. Checks:
        - For both periods (Daily and Weekly)
        - Ensures that a habit has not already been completed. Returns to main if true
        - Sets the streak to 1 if the habit has been completed out of the time frame for the period
        - Increments the streak if the habit has been completed within the time frame for the period
    :param habit: Receives an instance of the class Habits. User defined name and period
    :return: N/A : Simply updates the DB to set the completion field. List of habits is updated with display-habit
    """

    cursor_db.execute("SELECT * FROM Habits WHERE name = ? AND periodicity = ?",
                      [habit.habit_name, habit.habit_periodicity])

    row = cursor_db.fetchone()
    if row is None:
        print("No such Habit and Period combination")
        return

    habit = Habits(habit_name=row[0], habit_periodicity=row[1], habit_number=row[2], habit_start_date=row[3],
                   habit_complete=row[4], habit_last_complete=row[5], habit_streak=row[6])

    habit.habit_last_complete = datetime.strptime(habit.habit_last_complete, "%Y-%m-%d %H:%M:%S")

    if habit.habit_periodicity == "daily":  # Check periodicity as it influences streak and completion updates
        if habit.habit_complete == 1:  # Check if the habit has already been completed for the day
            print("Habit completed for the day!")
            return  # return as no action should be taken
        day = timedelta(days=1)  # Determine the length of a day
        if (datetime.now().replace(microsecond=0) - habit.habit_last_complete) > day:  # Checks habit completed in time
            print("No streak")
            habit.habit_streak = 1  # Set to 1 as the habit has been completed so streak was 0 and is now 1
            cursor_db.execute("UPDATE Habits SET streak = 1, pastComplete = ?, completion = True WHERE name = ?",
                              [datetime.now().replace(microsecond=0), habit.habit_name])
        else:
            habit.habit_streak += 1  # Increment streak if completed on time
            cursor_db.execute("UPDATE Habits SET streak = ?, pastComplete = ?, completion = True WHERE name = ?",
                              [habit.habit_streak, datetime.now().replace(microsecond=0), habit.habit_name])
    elif habit.habit_periodicity == "weekly":  # Similar procedure conducted for a weekly period
        if habit.habit_complete == 1:
            print("Habit completed for the week!")
            return
        week = timedelta(days=7)  # Determines the length of a week
        if (datetime.now().replace(microsecond=0) - habit.habit_last_complete) > week:
            print("No streak")
            habit.habit_streak = 1
            cursor_db.execute("UPDATE Habits SET streak = 1, pastComplete = ?, completion = True WHERE name = ?",
                              [datetime.now().replace(microsecond=0), habit.habit_name])
        else:
            habit.habit_streak += 1
            cursor_db.execute("UPDATE Habits SET streak = ?, pastComplete = ?, completion = True WHERE name = ?",
                              [habit.habit_streak, datetime.now().replace(microsecond=0), habit.habit_name])
    connection_db.commit()  # Commit all changes to the DB