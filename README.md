# Auto-grader

This is an automated grader that evaluates students' grades. As of now it is structured into 3 parts:

- Auto-downloader: Downloads specified submissions from all students who submitted as ZIP file and extracts it into the 'autograder' directory. Script: `adam.py`
- Auto-grader: Takes downloaded hand-ins (Jupyter Notebooks of students) and performs otter-grader checks; summarizes results into a spreadsheet. Scripts: `main.py` and `insurance_analysis.py`
- [WORK-IN-PROGRESS] Auto-publisher: Publishes auto-graded results onto ADAM as feedback for the students.

#### Contents
- 1. Setup and Virtual Environment
- 2. Structure
  - 2.1 Structure of Auto-downloader
  - 2.2 Structure of Auto-grader
  - 2.3 Structure of Auto-publisher [WIP]

## 1. Setup and Virtual Environment
- Setup:
  - Clone repo, `cd autograder`

- Create and setup virtual environment:
  - Create virtual environment `python -m venv venv`
  - `source venv/bin/activate`
  - `pip3 install -r requirements.txt`
  - to quit virtual environment: `deactivate`

## 2. Structure
### 2.1 Structure of Auto-downloader
This is an automated downloader collecting a specific exercise from a specific coursesite on ADAM for all students that handed in something.

##### How To Run The Program

- Download specific exercise from specific course:
  - Optionally, start virtual environment:
    - `cd autograder`
    - `source venv/bin/activate`
  - `python3 adam.py -u USERNAME -p PASSWORD -n EXERCISENR`
    - optional args: coursesite, mode, ...; for help and list, see `python3 adam.py -h`
    - This script logs in and joins the default course page on ADAM and downloads all hand-ins from given exercise as zip file. It then unpacks and moves the hand-ins to the `autograder` directory as `autograder/EXERCISENAME/Abgaben/...`.

- To alter course and exercise infos for the download consult the TODOs in `adam.py`.

### 2.2 Structure of Auto-grader

The packages are:

- ``grader``
- `main.py`
- `analysis`

##### How To Run The Program

- Download all Hand-Ins from Adam and Extract in the **working directory**
- Copy all the necessary tests from the Insurance Week
- Then the execution must the following:
  - `main.py` If the programm is done, it returns a 0
    - It creates a feedback_YMD folder (Which has the otter grader output as feedback)
    - It has the raw grades:
      If all tests were correct: 1 1 1 for Question 1, Question 2, Question 3
      If one test failed eg. Question 1, the grading is: 0 1 1
      If all tests failed, then the output is 0 0 0 
      The names, e-mail, individual points are stored in: `grades_raw_YMD.csv`
  - To calculate the Bonus-Points and make a bar-plot use: `analysis.py`
    - This output is in the analysis folder

### 2.3 Structure of Auto-publisher

[WIP]