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

from cli_runner import Runner

import cli_commands_meta
import cli_commands_enrolment

runner = Runner()
cli_commands_meta.link(runner)
cli_commands_enrolment.link(runner)


if __name__ == '__main__':
    while True:
        print(runner.resolve_command(input('').strip()))
