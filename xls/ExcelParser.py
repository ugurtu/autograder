import pandas as pd

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"


class ExcelParser:

    def __init__(self, sheet_name, exercise_number, mode):
        self.sheet_name = sheet_name
        self.exercise_number = exercise_number
        self.mode = mode
        self.file_path = "../xls/exercise-and-insurance-points.xls"

    def get_data(self):
        xls = pd.ExcelFile(self.file_path)
        data = pd.read_excel(xls, self.sheet_name)
        return data

    """
    This merges the data of insurance_analysis.py namely:
    caalculated_points.csv and data from the excel file.
    If E-mail is present in both files, the data is merged.
    If not present, then it is just NaN. It gives a new xls file.
    
    """

    def merge_data(self):
        if self.mode == "-i":
            data2 = pd.read_csv(f'../insurance_analysis/Insurance_{self.exercise_number}_Results.csv')
            data2 = data2[["E-Mail", f"IP{self.exercise_number}_calc"]]

            merged_df = pd.merge(self.get_data(), data2, on="E-Mail", how="left")
            merged_df[f"IP{self.exercise_number}"] = merged_df[f"IP{self.exercise_number}_calc"].fillna(0)

            merged_df = merged_df.drop(f'IP{self.exercise_number}_calc', axis=1)
            merged_df.to_excel(f'../xls/Insurance_{self.exercise_number}_Results.xlsx', index=False)

            return merged_df
