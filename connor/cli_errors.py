"""
This module contains exceptions used in the commands and the command runner.
"""


class RunnerError(Exception):
    """
    RunnerError is a standard error that will print "ERROR: <message>" if
    raised in a CLI command.
    """
    pass
