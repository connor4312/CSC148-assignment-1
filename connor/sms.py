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

from cli.runner import Runner

import cli.commands.meta
import cli.commands.enrolment

runner = Runner()
cli.commands.meta.link(runner)
cli.commands.enrolment.link(runner)


if __name__ == '__main__':
    runner.run()
