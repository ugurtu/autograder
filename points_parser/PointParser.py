import re


# Read the script where the test case is defined

class PointParser:

    def question_parser(self, question_number):
        with open(f'../autograder/tests/Question {question_number}.py', 'r') as file:
            script_content = file.read()

        # Use regular expression to find the points value
        points_match = re.search(r'points\s*=\s*(\d+)', script_content)

        if points_match:
            points = int(points_match.group(1))
            return points
