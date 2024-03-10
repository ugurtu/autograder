import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"

"""
This is a class. To get the notebooks. This must downloaded from Adam.
And unpacked in the autograder directory.
It will be used to grade the students' assignments.
"""


class InsuranceAnalysis:

    def __init__(self, exercise_number, file_name, directory):
        self.directory = f'{directory}'
        self.filename = file_name
        self.exercise_number = exercise_number
        self.file_path = f"{directory}"

    def get_data(self):
        os.chdir(self.file_path)
        data = pd.read_csv(self.filename)
        self.compute_sum(data)
        self.compute_bonus(data)
        self.data_to_csv(data)

    def compute_sum(self, data):
        data['Points_Total'] = data['Question 1'] + data['Question 2'] + data['Question 3']
        return data

    def compute_bonus(self, data):
        data[f'IP{self.exercise_number}_calc'] = data['Points_Total'] / 3
        return data

    def data_to_csv(self, data):
        os.chdir("../insurance_analysis")
        data.to_csv(f'Insurance_{self.exercise_number}_Results.csv', index=False)

    def make_hist(self):
        data = pd.read_excel(f'../xls/Insurance_{self.exercise_number}_Results.xlsx')
        sns.set_theme(style="darkgrid")
        ax = plt.gca()
        # Set custom x-axis label
        ax.set_xlabel('Bonus Points')
        ax.set_ylabel('Number of Students')
        # TODO: Change every Time to IP1, IP2, IP3 and so on.
        # Maybe change later that we can choose the column later
        ## IP = Insurance Points = Ex_Number -1

        sns.barplot(data[f'IP{self.exercise_number}'].value_counts(), ax=ax, alpha=0.8)
        plt.title('Statistics')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.3f}'.format(x / 3)))
        plt.savefig('histogram.png')
        plt.show()