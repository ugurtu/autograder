# Auto-Downloader
This is an automated downloader collecting a specific exercise from a specific coursesite on ADAM for all students that handed in something.

#### How To Run The Program

- Create and setup virtual environment:
  - Clone repo, 'cd autograder'.
  - Create virtual environment 'python -m venv venv'
  - 'source venv/bin/activate'
  - 'pip3 install -r requirements.txt'
  - to quit virtual environment: 'deactivate'

- Download specific exercise from specific course:
  - start virtual environment:
    - 'cd autograder'
    - 'source venv/bin/activate'
  - 'python3 adam.py -u USERNAME -p PASSWORD -n EXERCISENR'
    - optional args: coursesite, mode, ...; for help see 'python3 adam.py -h'
    - This script logs in and joins the default course page on ADAM and downloads all hand-ins from given exercise as zip file. It then unpacks and moves the hand-ins to the 'autograder' directory as 'autograder/EXERCISENAME/Abgaben/...'.




