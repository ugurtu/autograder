from datetime import datetime, timedelta


# First hand-in date for the exercise

class NumberOfExercise:

    def __init__(self):
        self.year = 2024
        self.month = 2
        self.day = 28
        self.timedelta = None
        # Create the datetime object with the specified date and time

    def get_number_of_exercise(self):
        desired_datetime = datetime(self.year, self.month, self.day)
        self.timedelta = datetime.now() - desired_datetime

        if self.timedelta.days < 7:
            return 1
        elif self.timedelta.days < 14:
            return 2
        elif self.timedelta.days < 21:
            return 3
        elif self.timedelta.days < 28:
            return 4
        elif self.timedelta.days < 35:
            return 5
        elif self.timedelta.days < 42:
            return 6
        elif self.timedelta.days < 49:
            return 7
        elif self.timedelta.days < 56:
            return 8
        elif self.timedelta.days < 63:
            return 9
        elif self.timedelta.days < 70:
            return 10

