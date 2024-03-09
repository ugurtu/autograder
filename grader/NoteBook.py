import os
from exercise_number_calculator.number_of_exercise import NumberOfExercise

"""
__author__ = "Ugur Turhal","Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch","mark.starzynski@unibas.ch"

This is a class. To get the notebooks. This must downloaded from Adam.
And unpacked in the autograder directory.
It will be used to grade the students' assignments.
"""


class NoteBook:
    """
    This class will be used to grade the students' assignments.
    """

    def __init__(self,arg):
        self.exercise_number = NumberOfExercise().get_number_of_exercise()
        if arg == "-e":
            self.main_directory = f'Exercise sheet {self.exercise_number}/Abgaben'
        elif arg == "-i":
            # This is for the insurance the number of the exercise is the same as the insurance number
            self.main_directory = f'Insurance {self.exercise_number}/Abgaben'

    """
    This function finds all notebooks in subdirectories.
    :return: list of notebooks
    """

    # Function to recursively find notebooks in subdirectories
    def find_notebooks(self):
        notebooks = []
        for root, dirs, files in os.walk(self.main_directory):
            for file in files:
                if file.endswith('.ipynb'):
                    # New file name
                    # This is for UNIX systems
                    # Linux
                    root = root.replace(' ', '\ ')
                    """
                    Comment in to see what the path is.
                    Maybe We have to change the path for windows
                    
                    Then we have to first to check what the OS is
                    and then change the path.
                    """
                    # print(os.path.join(root, file))

                    notebooks.append(os.path.join(root, file))

        return notebooks
