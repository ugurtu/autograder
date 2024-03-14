import os


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

    def __init__(self, arg):
        # arg[0] is the mode -e or -i
        # arg[1] is the exercise_number number or insurance number
        self.mode = arg[0]
        self.exercise_number = arg[1]
        if arg[0] == "-e":
            self.main_directory = f'Exercise sheet {self.exercise_number}/Abgaben'
        elif arg[0] == "-i":
            # This is for the insurance the number of the exercise_number is the same as the insurance number
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
                    # This method prevents that the test fails,
                    # if someone has a late submission, for that
                    # we have to rename the file to the exercise_number number
                    # @self.exercise_numberNAMEOFNOTEBOOKYEAR.ipynb
                    # since we have also a leading 0 we have to check if the exercise_number number is smaller than 10
                    name = ""
                    if self.mode == "-e":
                        if int(self.exercise_number) < 10:
                            name = f"{0}{self.exercise_number}exercisepids2024.ipynb"
                        elif int(self.exercise_number) >= 10:
                            name = f"{self.exercise_number}exercisepids2024.ipynb"

                    elif self.mode == "-i":
                        if int(self.exercise_number):
                            name = f"insurance{self.exercise_number}.ipynb"

                    os.rename(os.path.join(root, file), os.path.join(root, name))
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
