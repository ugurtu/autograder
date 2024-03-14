import pandas as pd
import os


class WriterDataBaseOffline:

    def __init__(self, exercise_number, mode):
        self.database = pd.read_csv('../autograder/localdb/Exercises.csv')
        self.exercise_number = exercise_number
        self.mode = mode

    def write_total(self, points):
        if self.mode == "-i":
            data = pd.read_csv("../autograder/localdb/Points_Insurance.csv")
            data[f"IP{self.exercise_number}"] = points/3
            total = data.loc[:, f'IP1':'IP11'].sum(axis=1)
            data['IP_Total'] = total
            data.to_csv("../autograder/localdb/Points_Insurance.csv", index=False)

        elif self.mode == "-e":
            data = pd.read_csv("../autograder/localdb/Points.csv")
            data[f"Ex{self.exercise_number}"] = points
            total = data.loc[:, f'Ex{self.exercise_number}':f'Ex{self.exercise_number}'].sum(axis=1)
            data['Exercise_Total'] = total
            data.to_csv("../autograder/localdb/Points.csv", index=False)

    def write(self):

        if self.mode == "-e":
            data2 = pd.read_csv(f'analysis/Exercise_Analysis_{self.exercise_number}/Exercise_{self.exercise_number}_Results.csv')
            data2 = data2[["E-Mail", f"Points_Total"]]
            merged_df = pd.merge(self.database, data2, on="E-Mail", how="left")
            merged_df[f"Ex{self.exercise_number}"] = merged_df["Points_Total"].fillna(0)
            merged_df = merged_df.drop("Points_Total", axis=1)

            total_points = merged_df.loc[:, f'Ex2':'Ex11'].sum(axis=1)
            # Update the IP_Total column with the calculated total
            merged_df['Ex_achieved'] = total_points

            merged_df.to_csv(f'../autograder/localdb/Exercises.csv', index=False)

            exercise_df = pd.read_csv(f'../autograder/localdb/Exercises.csv')
            points_insurance_df = pd.read_csv(f'../autograder/localdb/Points.csv')

            ip = f'Ex{self.exercise_number}'
            parent_folder = f'analysis/Exercise_Analysis_{self.exercise_number}/Feedback_Exercise {self.exercise_number}'

            for subdir, dirs, files in os.walk(parent_folder):
                for file in files:
                    mail, _ = file.split("_")

                    # Assuming you have DataFrames `exercises_df` and `points_ip_df` containing your data
                    exercise_row = exercise_df[exercise_df['E-Mail'] == mail]
                    points_row = points_insurance_df["Exercise_Total"].iloc[0]

                    if not exercise_row.empty:
                        ex = exercise_row[ip].iloc[0]
                        ip_achieved = exercise_row['Ex_achieved'].iloc[0]
                        ex_total = points_row

                        s = f"\nYou achieved in the Exercise {self.exercise_number}, {ex} points.\nThe total sum of your hand-in is: {ip_achieved}, of {ex_total} Points"
                        with open(f"{parent_folder}/{mail}_feedback.txt", "a") as write_file:
                            write_file.write(s)


        elif self.mode == "-i":
            data2 = pd.read_csv(f'analysis/Insurance_Analysis_{self.exercise_number}/Insurance_{self.exercise_number}_Results.csv')
            print(self.exercise_number)
            data2 = data2[["E-Mail", f"IP{self.exercise_number}_calc"]]
            merged_df = pd.merge(self.database, data2, on="E-Mail", how="left")
            merged_df[f"IP{self.exercise_number}"] = merged_df[f"IP{self.exercise_number}_calc"].fillna(0)
            merged_df = merged_df.drop(f'IP{self.exercise_number}_calc', axis=1)

            total_points = merged_df.loc[:, f'IP1':'IP11'].sum(axis=1)
            # Update the IP_Total column with the calculated total
            merged_df['IP_achieved'] = total_points
            merged_df.to_csv(f'../autograder/localdb/Exercises.csv', index=False)

            exercise_df = pd.read_csv(f'../autograder/localdb/Exercises.csv')
            points_insurance_df = pd.read_csv(f'../autograder/localdb/Points_Insurance.csv')

            ip = f'IP{self.exercise_number}'
            parent_folder = f'analysis/Insurance_Analysis_{self.exercise_number}/Feedback_Insurance {self.exercise_number}'
            for subdir, dirs, files in os.walk(parent_folder):
                for file in files:
                    mail, _ = file.split("_")

                    # Assuming you have DataFrames `exercises_df` and `points_ip_df` containing your data
                    exercise_row = exercise_df[exercise_df['E-Mail'] == mail]
                    points_row = points_insurance_df["IP_Total"].iloc[0]

                    if not exercise_row.empty:
                        ip1 = exercise_row[ip].iloc[0]
                        ip_achieved = exercise_row['IP_achieved'].iloc[0]
                        ip_total = points_row

                        s = f"\nYou achieved in the insurance exam: {ip1} point.\nThe total sum of your hand-in is: {ip_achieved}, of {ip_total} Points"
                        with open(f"{parent_folder}/{mail}_feedback.txt", "a") as write_file:
                            write_file.write(s)

