import os
import pandas as pd
from localdb.WriterDataBaseOflline import WriterDataBaseOffline

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"


class ExcelParser:

    def __init__(self, sheet_name, exercise_number, mode):
        self.sheet_name = sheet_name
        self.exercise_number = exercise_number
        self.mode = mode
        os.chdir("../..")
        self.file_path = 'xls/exercise-and-insurance-points.xls'

    def get_data(self):
        xls = pd.ExcelFile(self.file_path)
        data = pd.read_excel(xls, self.sheet_name)
        return data

    """
    This merges the data of analysis.py namely:
    calculated_points.csv and data from the excel file.
    If E-mail is present in both files, the data is merged.
    If not present, then it is just NaN. It gives a new xls file.
    
    """

    def merge_data(self):
        if self.mode == "-i":
            data2 = pd.read_csv(
                f'analysis/Insurance_Analysis_{self.exercise_number}/Insurance_{self.exercise_number}_Results.csv')
            data2 = data2[["E-Mail", f"IP{self.exercise_number}_calc"]]

            merged_df = pd.merge(self.get_data(), data2, on="E-Mail", how="left")
            merged_df[f"IP{self.exercise_number}"] = merged_df[f"IP{self.exercise_number}_calc"].fillna(0)

            merged_df = merged_df.drop(f'IP{self.exercise_number}_calc', axis=1)
            merged_df.to_excel(
                f'../autograder/analysis/Insurance_Analysis_{self.exercise_number}/Insurance_{self.exercise_number}_Results.xlsx',
                index=False)

            write_result = WriterDataBaseOffline(self.exercise_number, self.mode)
            write_result.write()
            os.remove(f'../autograder/.OTTER_LOG')
            return merged_df

        if self.mode == "-e":
            data2 = pd.read_csv(
                f'analysis/Exercise_Analysis_{self.exercise_number}/Exercise_{self.exercise_number}_Results.csv')
            data2 = data2[["E-Mail", "Points_Total"]]
            merged_df = pd.merge(self.get_data(), data2, on="E-Mail", how="left")
            merged_df[f"Ex{self.exercise_number}"] = merged_df["Points_Total"].fillna(0)
            merged_df = merged_df.drop("Points_Total", axis=1)
            merged_df.to_excel(
                f'../autograder/analysis/Exercise_Analysis_{self.exercise_number}/Exercise_{self.exercise_number}_Results.xlsx',
                index=False)

            write_result = WriterDataBaseOffline(self.exercise_number, self.mode)
            write_result.write()
            os.remove(f'../autograder/.OTTER_LOG')
            return merged_df
