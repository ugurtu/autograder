import re

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"
__date__ = "2024/03/13"
__version__ = "1.0.0"


# Read the script where the test case is defined


class PointParser:

    def __init__(self):
        self.max_points = 0

    def question_parser(self, question_number):
        with open(f'../autograder/tests/Question {question_number}.py', 'r') as file:
            script_content = file.read()

        # Use regular expression to find the points value
        points_match = re.search(r'points\s*=\s*(\d+)', script_content)

        if points_match:
            points = int(points_match.group(1))
            self.max_points += points
            return points

    def max_points(self):
        return self.max_points
