"""
This module's "link" function binds the meta enrolment commands to the test
runner. By invoking link(Runner), the following commands become available:

    >>> exit
    exits the sms process

    >>> undo <number=1>
    reverse the last command or last <number> of commands

See each commands individual docstring for return details.
"""
import sys
from cli_errors import RunnerError
from somewhatDb_database import db


def link(runner):
    """ (Runner) -> NoneType
    Binds "meta" commands to the task runner.
    """

    @runner.command('exit')
    def exit_loop():
        """ () -> NoneType
        Exits the process. Example usage:

            > exit
        """
        sys.exit()

    @runner.command('undo')
    def undo(actions=1):
        """ (int) -> string
        Undoes the given number of actions. If there are no commands
        left to undo, then it returns an error. Example usage:

            > undo
            > undo 3
        """

        def raise_number_error():
            """ () -> NoneType
            Raises a "x is not a positive natual number" error.
            """
            raise RunnerError('%s is not a positive natural number.' % actions)

        try:
            actions = int(actions)
        except ValueError:
            raise_number_error()

        if actions < 0:
            raise_number_error()

        if db.undo_count() < actions:
            raise RunnerError('No commands to undo.')

        for x in range(actions):
            db.undo()

        return ''
