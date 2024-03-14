import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

__author__ = "Ugur Turhal","Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch","mark.starzynski@unibas.ch"
__date__ = "2024/03/13"
__version__ = "1.0.0"

"""
This is a class. To get the notebooks. This must downloaded from Adam.
And unpacked in the autograder directory.
It will be used to grade the students' assignments.
"""


class InsuranceAnalysis:

    def __init__(self, exercise_number, file_name, mode, number_of_questions):
        self.filename = file_name
        self.exercise_number = exercise_number
        self.mode = mode
        self.number_of_questions = number_of_questions

        """
        Distinguish between the modes.
        if self.mode == i then insurance + Exercise Nr. 1
        if self.mode == e then exercise_number + Exercise Nr. 2
        """
        if self.mode == "-i":
            os.chdir(f"../autograder/analysis/Insurance_Analysis_{self.exercise_number}")

        elif self.mode == "-e":
            os.chdir(f"../autograder/analysis/Exercise_Analysis_{self.exercise_number}")


    def get_data(self):

        data = pd.read_csv(self.filename)
        self.compute_sum(data)
        self.compute_bonus(data)
        self.data_to_csv(data)

    """
    Can be used for both.
    The data is the filename which we gave in the NoteBookGrader.py
    
    """
    def compute_sum(self, data):

        questions_to_sum = [key for key in data.keys() if key.startswith('Question')]

        total_points = 0
        for question in questions_to_sum:
            total_points += data[question]
            data['Points_Total'] = total_points

        return data

    """
    The bonus point is only needed for the insurance points.
    The exercise_number points are already calculated.
    """
    def compute_bonus(self, data):
        if self.mode == "-i":
            data[f'IP{self.exercise_number}_calc'] = data['Points_Total'] / 3

        return data

    def data_to_csv(self, data):
        """
        Is needed for both. But we have to distinguish between the modes.

        """
        if self.mode == "-i":
            data.to_csv(f'Insurance_{self.exercise_number}_Results.csv', index=False)
        elif self.mode == "-e":
            data.to_csv(f'Exercise_{self.exercise_number}_Results.csv', index=False)

    def make_hist(self):
        data = pd.read_excel(f'analysis/Insurance_Analysis_{self.exercise_number}/Insurance_{self.exercise_number}_Results.xlsx')
        sns.set_theme(style="darkgrid")
        ax = plt.gca()
        # Set custom x-axis label
        ax.set_xlabel('Bonus Points')
        ax.set_ylabel('Number of Students')

        sns.barplot(data[f'IP{self.exercise_number}'].value_counts(), ax=ax, alpha=0.8)
        plt.title('Statistics')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.3f}'.format(x / 3)))
        plt.savefig(f'analysis/Insurance_Analysis_{self.exercise_number}/Histogram_Insurance_{self.exercise_number}.png')
        # plt.show()

    def exercise_evaluation(self):
        data = pd.read_excel(f'analysis/Exercise_Analysis_{self.exercise_number}/Exercise_{self.exercise_number}_Results.xlsx')
        sns.set_theme(style="darkgrid")
        ax = plt.gca()
        # Set custom x-axis label
        ax.set_xlabel('Received Points')
        ax.set_ylabel('Number of Students')

        #Barplot
        sns.barplot(data[f'Ex{self.exercise_number}'].value_counts(), ax=ax, alpha=0.8)
        plt.title('Statistics')
        plt.savefig(f'analysis/Exercise_Analysis_{self.exercise_number}/Histogram_Exercise_{self.exercise_number}.png')
