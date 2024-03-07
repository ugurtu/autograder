# Auto-grader
This is an automated grader that evaluates students' grades.

### Structure

The packages are:

- ``grader``
- `main.py`
- `analysis`

#### How To Run The Program

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

