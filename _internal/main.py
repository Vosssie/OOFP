from datetime import datetime  # To determine the current date and time


class Habits:

    # Class defined to store all relevant habit information:
    #   - habit_name        → Stores the name of the habit
    #   - habit_periodicity → Stores the period of the habit (daily or weekly)
    #   - habit_number      → Stores the number of the habit (The order that the habit was created)
    #   - habit_start_date  → Stores the day (YYYY-MM-DD) and time(HH-MM-SS) that a habit was created
    #   - habit_complete    → Stores whether a habit has been completed during the time period or not
    #   - habit_last_complete → Stores the day (YYYY-MM-DD) and time(HH-MM-SS) that a habit was last completed
    #   - habit_streak      → Stores the streak count for a habit

    def __init__(self, habit_name, habit_periodicity, habit_number=None, habit_start_date=None, habit_complete=None,
                 habit_last_complete=None, habit_streak=None):

        self.habit_name = habit_name  # Default value for habit name (Habit always has a name when created)
        self.habit_periodicity = habit_periodicity  # Default value for period (Habit always has a period when created)
        if habit_number is None:  # If there is no value, then assign a default value
            self.habit_number = 0
        else:
            self.habit_number = habit_number
        if habit_start_date is None:
            self.habit_start_date = datetime.now().date()  # Default start date is the current date and time
        else:
            self.habit_start_date = habit_start_date
        if habit_complete is None:
            self.habit_complete = 0  # Default is zero (Not complete). 1 is complete.
        else:
            self.habit_complete = habit_complete
        if habit_last_complete is None:
            self.habit_last_complete = None
        else:
            self.habit_last_complete = habit_last_complete
        if habit_streak is None:
            self.habit_streak = 0  # Streak is defaulted to zero
        else:
            self.habit_streak = habit_streak

    def __repr__(self):  # Method

        # Default return string if an Instance of the Habit class is printed
        # Default tab spacing is outlined to ensure ease of reading of the information

        return (f"{self.habit_name:<{20}} {self.habit_periodicity:<{10}} {str(self.habit_number):<{10}} "
                f"{str(self.habit_start_date):<{25}} {str(self.habit_complete):<{10}} "
                f"{str(self.habit_last_complete):<{25}} {str(self.habit_streak):<{10}}")


