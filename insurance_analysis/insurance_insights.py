import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from xls.excel_parser import ExcelParser

__author__ = "Ugur Turhal","Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch","mark.starzynski@unibas.ch"

"""
This is a class. To get the notebooks. This must downloaded from Adam.
And unpacked in the autograder directory.
It will be used to grade the students' assignments.
"""

def get_data():
    os.chdir("..")
    data = pd.read_csv('grades_raw_'+time.strftime("%y%m%d") +'.csv')
    return data


def compute_sum(data):
    data['Points_Total'] = data['Question 1'] + data['Question 2'] + data['Question 3']
    return data


def compute_bonus(data):
    data['Points_Total'] = data['Points_Total'] / 3
    return data


def data_to_csv(data):
    os.chdir("insurance_analysis")
    data.to_csv('calculated_points.csv', index=False)


def make_hist(data):
    sns.set_theme(style="darkgrid")
    ax = plt.gca()

    # Set custom x-axis label
    ax.set_xlabel('Bonus Points')
    ax.set_ylabel('Number of Students')
    # TODO: Change every Time to IP1, IP2, IP3 and so on.
    # Maybe change later that we can choose the column later
    
    sns.barplot(data['IP1'].value_counts(), ax=ax, alpha=0.8)
    plt.title('Statistics')
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.3f}'.format(x / 3)))
    plt.savefig('histogram.png')
    plt.show()


if __name__ == '__main__':
    data = get_data()
    data = compute_sum(data)
    data = compute_bonus(data)
    data_to_csv(data)
    make_hist(ExcelParser().merge_data())