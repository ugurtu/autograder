import os

import mysql.connector
import pandas as pd

__author__ = "Ugur Turhal", "Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch", "mark.starzynski@unibas.ch"
__date__ = "2024/03/13"
__version__ = "1.0.0"


class MySQLPumper:

    def __init__(self):
        self.connector = mysql.connector.connect(
            host=...,
            user=...,
            password=...,
            database=...
        )
        self.mode = ""
        self.exercise_number = 0
        # Needed in pump_exercise method!
        # We have to specify it like f'IP{exercise_number}'
        # Or f'IP{exercise_number}'
        self.ex_number = ""

    def pump_ip(self, exercise_number: int, modes: str):
        self.mode = modes

        if self.mode == "-i":
            data = pd.read_excel(
                f'analysis/Insurance_Analysis_{exercise_number}/Insurance_{exercise_number}_Results.xlsx',
                engine='openpyxl')
            ip_number = f"IP{exercise_number}"

            for i in range(len(data)):
                e_mail = data[f"E-Mail"][i]
                points = data[ip_number][i]
                cursor = self.connector.cursor()
                query = f'UPDATE Exercises SET {ip_number} = %s WHERE email = %s'
                cursor.execute(query, (points, e_mail))
                self.connector.commit()

        if self.mode == "-e":
            data = pd.read_excel(
                f'analysis/Exercise_Analysis_{exercise_number}/Exercise_{exercise_number}_Results.xlsx',
                engine='openpyxl')
            data = data[:176]
            ip_number = f"Ex{exercise_number}"

            for i in range(len(data)):
                e_mail = data[f"E-Mail"][i]
                points = int(data[ip_number][i])
                cursor = self.connector.cursor()
                query = f'UPDATE Exercises SET {ip_number} = %s WHERE email = %s'
                cursor.execute(query, (points, e_mail))
                self.connector.commit()

    def pump_exercise(self, exercise_number: int, modes: str) -> None:
        if modes == "-i":
            data = pd.read_excel(
                f'analysis/Insurance_Analysis_{exercise_number}/Insurance_{exercise_number}_Results.xlsx',
                engine='openpyxl')
            self.ex_number = f"IP{exercise_number}"

        elif modes == "-e":
            data = pd.read_excel(
                f'analysis/Exercise_Analysis_{exercise_number}/Exercise_{exercise_number}_Results.xlsx',
                engine='openpyxl')

            self.ex_number = f"Ex{exercise_number}"

        for i in range(len(data)):
            e_mail = data["E-Mail"][i]
            points = data[self.ex_number][i]
            query = f'UPDATE Exercises SET {self.ex_number} = %s WHERE email = %s'
            self.connector.cursor().execute(query, (points, e_mail))
            self.connector.commit()

    def max_points(self, points, modes, exercise_number):
        self.mode = modes
        self.exercise_number = exercise_number

        if self.mode == "-i":
            ip = f"IP{exercise_number}"
            points_ip = "Points_IP"
            query = f'UPDATE {points_ip} SET {ip} = %s'
            self.connector.cursor().execute(query, (points / 3,))
            self.connector.commit()

        if self.mode == "-e":
            ip = f"Ex{exercise_number}"
            query = f'UPDATE Points SET {ip} = %s'
            self.connector.cursor().execute(query, (points,))
            self.connector.commit()

    def retrieve_points(self, modes: str, exercise_number: int):
        if modes == "-i":
            print("Writing points for Feedback_Insurance")
            ip = f"IP{exercise_number}"
            parent_folder = f'analysis/Insurance_Analysis_{exercise_number}/Feedback_Insurance {exercise_number}'
            for subdir, dirs, files in os.walk(parent_folder):
                for file in files:
                    mail, _ = file.split("_")
                    query = f"""
                        SELECT e.{ip}, e.IP_achieved, ip.IP_Total
                        FROM Exercises e, Points_IP ip
                        WHERE e.email = '{mail}'
                    """
                    cursor = self.connector.cursor()
                    cursor.execute(query)
                    results = cursor.fetchall()  # Fetch all results before executing another query
                    for row in results:
                        ip1, ip_achieved, ip_total = row
                        s = f"\nYou achieved in the insurance exam: {ip1} point.\nThe total sum of your hand-in is: {ip_achieved}, of {ip_total} Points"
                        with open(f"{parent_folder}/{mail}_feedback.txt", "a") as file:
                            file.write(s)

        if modes == "-e":
            ex = f"Ex{exercise_number}"
            parent_folder = f'analysis/Exercise_Analysis_{exercise_number}/Feedback_Exercise {exercise_number}'
            for subdir, dirs, files in os.walk(parent_folder):
                for file in files:
                    mail, _ = file.split("_")
                    query = f"""
                        SELECT e.{ex}, e.Ex_achieved, p.Exercise_Total
                        FROM Exercises e, Points p
                        WHERE e.email = '{mail}'
                    """
                    cursor = self.connector.cursor()
                    cursor.execute(query)
                    results = cursor.fetchall()  # Fetch all results before executing another query
                    for row in results:
                        ip1, ip_achieved, ip_total = row
                        s = f"\nYou achieved in the Exercise {exercise_number}, {ip1} points.\nThe total sum of your hand-in is: {ip_achieved}, of {ip_total} Points"
                        with open(f"{parent_folder}/{mail}_feedback.txt", "a") as file:
                            file.write(s)
        self.connector.close()
