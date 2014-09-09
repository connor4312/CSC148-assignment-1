# Assignment 1 - Managing students!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""Interactive console for assignment.

This module contains the code necessary for running the interactive console.
As provided, the console does nothing interesting: it is your job to build
on it to fulfill all the given specifications.

run: Run the main interactive loop.
"""

import sys
from cli.runner import Runner

runner = Runner()


@runner.command('exit')
def exit():
    sys.exit()


@runner.command('create student')
def creates(name):
    return 'Created student ' + name


if __name__ == '__main__':
    runner.run()