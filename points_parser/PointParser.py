import re
import os

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"
__date__ = "2024/03/13"
__version__ = "1.0.0"


# Read the script where the test case is defined


class PointParser:

    def __init__(self):
        self.max_points = 0

    def get_questions(self):
        print(os.getcwd())
        list_of_files = []
        for filename in os.listdir('tests'):
            # Check if the file is a Python file
            if filename.endswith('.py'):
                # Construct the full path to the file
                list_of_files.append(filename.replace('.py', ''))

        return list_of_files
        # Open and read the file content

    def question_parser(self, question_number):
        with open(f'tests/{question_number}.py', 'r') as file:
            script_content = file.read()

        # Use regular expression to find the points value
        points_match = re.search(r'points\s*=\s*(\d+)', script_content)

        if points_match:
            points = int(points_match.group(1))
            self.max_points += points
            return points

    def max_points(self):
        return self.max_points
