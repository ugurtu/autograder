# Auto-Downloader
This is an automated downloader collecting a specific exercise from a specific coursesite on ADAM for all students that handed in something.

#### How To Run The Program

- Create and setup virtual environment:
  - Clone repo, 'cd autograder'.
  - Create virtual environment 'python -m venv venv'
  - 'source venv/bin/activate'
  - 'pip install -r requirements.txt'
  - to quit virtual environment: 'deactivate'

- Download specific exercise from specific course:
  - start virtual environment:
    - 'cd autograder'
    - 'source venv/bin/activate'
  - 'python adam.py -u USERNAME -p PASSWORD -n EXERCISENR'
    - optional args: coursesite, mode, ..., for help see 'python adam.py -h'
    - This script logs in and joins the default course page on ADAM and downloads all hand-ins from given exercise as zip file. It then unpacks and moves the hand-ins to the 'autograder/' directory as 'EXERCISENAME/Abgaben/...'.




