import shutil
import subprocess
import csv
import re
import os
import time
from analysis.Analysis import InsuranceAnalysis
from xls.ExcelParser import ExcelParser
from points_parser.PointParser import PointParser

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"

"""
This is the NoteBookGrader class.
It will be used to grade the students' assignments.
"""


class NoteBookGrader:
    """
    This will grade the notebooks
    """

    def __init__(self, notebooks, mode):
        self.mode = mode[0]
        self.notebooks = notebooks
        self.tests = 'tests'
        self.number_of_questions = 0
        self.exercise_number = mode[1]
        self.question_points = {}
        if self.mode == "-e":
            self.output_csv_file = time.strftime("%y%m%d") + f'_CSV_Grades_Exercise_{self.exercise_number}' + ".csv"
        elif self.mode == "-i":
            self.output_csv_file = time.strftime("%y%m%d") + f'_CSV_Grades_Insurance_{self.exercise_number}' + ".csv"

    def create_feedback_folder(self):
        if self.mode == "-e":
            if not os.path.exists(f"Feedback_Exercise {self.exercise_number}"):
                os.makedirs(f"Feedback_Exercise {self.exercise_number}")

        elif self.mode == "-i":
            if not os.path.exists(f"Feedback_Insurance {self.exercise_number}"):
                os.makedirs(f"Feedback_Insurance {self.exercise_number}")

    def grade_notebooks(self):
        self.create_feedback_folder()

        with open(self.output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            num_files = len(
                [filename for filename in os.listdir(self.tests) if os.path.isfile(os.path.join(self.tests, filename))])
            self.number_of_questions = num_files
            # Write header row
            header_row = ['Family Name', 'Name', 'E-Mail', 'Adam-Number']

            """
            Parse the points here we use the class
            PointParser. Then iterate through a 
            """
            point = PointParser()

            for i in range(1, num_files + 1):
                header_row.append(f'Question {i}')
                self.question_points[f"Question {i}"] = point.question_parser(i)
            # print(self.question_points)
            max_points = 0

            for key, value in self.question_points.items():
                max_points += value
            """
            Pump the max points to the database
            """

            writer.writerow(header_row)
            counter = 1

            # Iterate over each notebook
            for notebook in self.notebooks:
                print(f"Starting grading on Notebook {counter} out of {len(self.notebooks)}...")
                counter += 1

                folder_name = os.path.basename(os.path.dirname(notebook))
                name, family_name, student_email, matriculation_number = "", "", "", ""
                folder_name = folder_name.split('_')

                if len(folder_name) == 4:
                    name, family_name, student_email, matriculation_number = folder_name
                    name = name.replace('\ ', ' ')
                    family_name = family_name.replace('\ ', ' ')

                else:
                    name = folder_name[0]
                    name = name.replace('\ ', ' ')
                    family_name = folder_name[2] + ' ' + folder_name[3]
                    family_name = family_name.replace('\ ', ' ')

                    student_email = folder_name[4]
                    matriculation_number = folder_name[5]

                notebook_grades = [name, family_name, student_email, matriculation_number]

                # Execute the otter check command
                command = f'otter check {notebook}'
                output = subprocess.check_output(command, shell=True, encoding='utf-8')
                current_directory = os.getcwd()

                if self.mode == "-e":
                    os.chdir(f"Feedback_Exercise {self.exercise_number}")
                elif self.mode == "-i":
                    os.chdir(f"Feedback_Insurance {self.exercise_number}")

                f = open(student_email + "_feedback.txt", "w+")
                f.write(output)
                f.close()
                # Change the directory back to the original directory
                # os.chdir(current_directory)

                # Extract the grade from the output for each question
                for i in range(1, self.number_of_questions + 1):
                    pattern_failed = fr'Question {i} - \d+ result:\s+❌ Test case failed.+'
                    match_failed = re.search(pattern_failed, output)
                    if match_failed:
                        notebook_grades.append(0)
                    else:
                        # Check if "All tests passed!" pattern is found
                        if "All tests passed!" in output:

                            points = self.question_points[f'Question {i}']
                            notebook_grades.append(points)
                        else:
                            # Check if specific question pattern is found
                            pattern_passed = fr'Question {i} results: All test cases passed!'
                            match_passed = re.search(pattern_passed, output)
                            if match_passed:
                                points = self.question_points[f'Question {i}']
                                notebook_grades.append(points)
                            else:
                                notebook_grades.append(0)

                # print("Correction Done", name, family_name, student_email, matriculation_number)
                # Write the row for this notebook to the CSV file
                writer.writerow(notebook_grades)
                os.chdir(current_directory)

        if self.mode == "-e":
            cwd = os.getcwd()
            """
            Create Subdirectory for every Exercise assignment
            """
            if os.path.exists(f"../autograder/analysis/Exercise_Analysis_{self.exercise_number}"):
                shutil.rmtree(f"../autograder/analysis/Exercise_Analysis_{self.exercise_number}")

            os.chdir("../autograder/analysis")
            os.mkdir(f"Exercise_Analysis_{self.exercise_number}")
            os.chdir(cwd)

            """
            Move the Output to the specific folder.
            """
            shutil.move("../autograder/" + self.output_csv_file,
                        f"analysis/Exercise_Analysis_{self.exercise_number}/{self.output_csv_file}")

            shutil.move(f"Feedback_Exercise {self.exercise_number}",
                        f"../autograder/analysis/Exercise_Analysis_{self.exercise_number}")

            analysis = InsuranceAnalysis(self.exercise_number, self.output_csv_file,
                                         "-e", self.number_of_questions)
            analysis.get_data()

            """
            Parse the data
            """
            excel_parser = ExcelParser("Exercises", self.exercise_number, self.mode)
            excel_parser.merge_data()

            analysis.exercise_evaluation()

        elif self.mode == "-i":
            cwd = os.getcwd()
            """
            Create Subdirectory for every insurance assignment
            
            """
            if os.path.exists(f"../autograder/analysis/Insurance_Analysis_{self.exercise_number}"):
                shutil.rmtree(f"../autograder/analysis/Insurance_Analysis_{self.exercise_number}")

            os.chdir("../autograder/analysis")
            os.mkdir(f"Insurance_Analysis_{self.exercise_number}")
            os.chdir(cwd)

            """
            Move the Output to the specific folder.
            """
            shutil.move("../autograder/" + self.output_csv_file,
                        f"analysis/Insurance_Analysis_{self.exercise_number}/{self.output_csv_file}")
            shutil.move(f"Feedback_Insurance {self.exercise_number}",
                        f"../autograder/analysis/Insurance_Analysis_{self.exercise_number}")

            analysis = InsuranceAnalysis(self.exercise_number, self.output_csv_file,
                                         "-i", self.number_of_questions)
            analysis.get_data()

            excel_parser = ExcelParser("Insurance", self.exercise_number, self.mode)
            excel_parser.merge_data()

            analysis.make_hist()
