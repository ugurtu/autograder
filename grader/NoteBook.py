import os

"""
This is a class. 
It will be used to grade the students' assignments.
__author__ = "Ugur Turhal","Mark Stranzky"
__email__ = "ugur.turhal@unibas.ch","mark.stranzky@unibas.ch"
"""


class NoteBook:
    """
    This class will be used to grade the students' assignments.
    """

    def __init__(self):
        self.main_directory = 'Abgaben'

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
