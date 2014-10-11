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
"""
Interactive console. Here is where everything comes together... we create a
runner and link the meta and enrolment commands to the runner. Finally, if this
is the main module, we start a loop that accepts console input, dispatches
it to the runner, and prints the output.
"""

from cli_runner import Runner

import cli_commands_meta
import cli_commands_enrolment

# Instantiate an instance of the CLI runner and link the commands to it.
runner = Runner()
cli_commands_meta.link(runner)
cli_commands_enrolment.link(runner)


def run():
    """ () -> NoneType
    If we called run... run forever and ever and ever.
    """

    while True:
        try:
            # Get input and send it over to the command parser.
            output = runner.resolve_command(input('').strip())

            # If we got some output, print it!
            if output is not None:
                print(output)

        except SystemExit:
            # Catch a systemexit and break. The autotester wants us to do
            # it this way, apparently.
            break


if __name__ == '__main__':
    run()
