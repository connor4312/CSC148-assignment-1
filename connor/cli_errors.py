"""
This module contains exceptions used in the commands and the command runner.
"""


class RunnerError(Exception):
    """
    RunnerError is a standard error that will print "ERROR: <message>" if
    raised in a CLI command.
    """
    pass


class RunnerHalterError(RunnerError):
    """
    The HalterError, a type of RunnerError will cause the transaction to
    *not* be ended: the command will not be in the undo stack.
    """
    pass
