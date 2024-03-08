from grader.NoteBook import NoteBook
from grader.NoteBookGrader import NoteBookGrader

"""
This is a class. 
It will be used to grade the students' assignments.
__author__ = "Ugur Turhal","Mark Starzynski"
__email__ = "ugur.turhal@unibas.ch","mark.starzynski@unibas.ch"
"""


def main():
    notebooks = NoteBook()
    notebooks = notebooks.find_notebooks()

    grader = NoteBookGrader(notebooks)
    grader.grade_notebooks()


if __name__ == "__main__":
    main()
