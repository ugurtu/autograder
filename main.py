import argparse
import sys
from grader.NoteBook import NoteBook
from grader.NoteBookGrader import NoteBookGrader

"""
This is a class. 
It will be used to grade the students' assignments.
__author__ = "Ugur Turhal","Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch","mark.starzynski@unibas.ch"
"""


def main():
    args = parse_args()
    notebooks = NoteBook(args)
    notebooks = notebooks.find_notebooks()

    grader = NoteBookGrader(notebooks)
    grader.grade_notebooks()


def parse_args():

    try:
        if sys.argv[1] not in ["-e", "-i"]:
            print("Please specify the mode with -e or -i. -e for exercise and -i for insurance.")
        else:
            return sys.argv[1]

    except Exception as e:
        print(f"Error parsing arguments: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
