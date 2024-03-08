import pandas as pd
import os

__author__ = "Ugur Turhal","Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch","mark.starzynski@unibas.ch"

class ExcelParser:


    def __init__(self):
        self.file_path = "../xls/exercise-and-insurance-points.xls"

    def get_data(self):
        xls = pd.ExcelFile(self.file_path)
        data = pd.read_excel(xls, 'Insurance')
        return data

    """
    This merges the data of insurance_analysis.py namely:
    caalculated_points.csv and data from the excel file.
    If E-mail is present in both files, the data is merged.
    If not present, then it is just NaN. It gives a new xls file.
    
    """

    def merge_data(self):
        data2 = pd.read_csv('../insurance_analysis/calculated_points.csv')
        data2 = data2[["E-Mail", "Points_Total"]]
        merged_df = pd.merge(self.get_data(), data2, on="E-Mail", how="left")

        # Fill NaN values in the Total Points column with 0
        merged_df["Points_Total"].fillna(0, inplace=True)
        # TODO: Change every Time to IP1, IP2, IP3 and so on.

        merged_df["IP1"] =merged_df["Points_Total"]

        merged_df = merged_df.drop('Points_Total', axis=1)
        # If you want to sum Total Points from CSV and Excel files, uncomment the following line
        # merged_df["Total Points"] = merged_df["Total Points_x"] + merged_df["Total Points_y"]

        merged_df.to_excel("merged_data.xlsx", index=False)

        return merged_df

