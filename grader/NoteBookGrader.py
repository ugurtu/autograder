import subprocess
import csv
import re
import os
import time

"""
This is the NoteBookGrader class.
It will be used to grade the students' assignments.
__author__ = "Ugur Turhal","Mark Stranzky"
__email__ = "ugur.turhal@unibas.ch","mark.stranzky@unibas.ch"
"""


class NoteBookGrader:
    """
    This will grade the notebooks
    """

    def __init__(self, notebooks):
        self.output_csv_file = 'grades_raw_'+time.strftime("%y%m%d")+".csv"
        self.notebooks = notebooks

    @staticmethod
    def create_feedback_folder():
        if not os.path.exists("feedback_"+time.strftime("%y%m%d")):
            os.makedirs("feedback_"+time.strftime("%y%m%d"))

    def grade_notebooks(self):
        self.create_feedback_folder()
        with open(self.output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row
            header_row = ['Family Name', 'Name', 'E-Mail', 'Adam-Number', 'Question 1', 'Question 2', 'Question 3']
            writer.writerow(header_row)

            # Iterate over each notebook
            for notebook in self.notebooks:

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

                os.chdir("feedback_"+time.strftime("%y%m%d"))
                f = open(student_email + "_feedback.txt", "w+")
                f.write(output)
                f.close()
                # Change the directory back to the original directory
                os.chdir(current_directory)

                # Extract the grade from the output for each question
                for i in range(1, 4):
                    pattern_failed = fr'Question {i} - \d+ result:\s+❌ Test case failed.+'
                    match_failed = re.search(pattern_failed, output)
                    if match_failed:
                        notebook_grades.append(0)
                    else:
                        # Check if "All tests passed!" pattern is found
                        if "All tests passed!" in output:
                            notebook_grades.append(1)
                        else:
                            # Check if specific question pattern is found
                            pattern_passed = fr'Question {i} results: All test cases passed!'
                            match_passed = re.search(pattern_passed, output)
                            if match_passed:
                                notebook_grades.append(1)
                            else:
                                notebook_grades.append(0)

                # print("Correction Done", name, family_name, student_email, matriculation_number)
                # Write the row for this notebook to the CSV file
                writer.writerow(notebook_grades)
                os.chdir(current_directory)