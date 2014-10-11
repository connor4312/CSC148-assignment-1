"""
This module's "link" function binds the meta enrolment commands to the test
runner. By invoking link(Runner), the following commands become available:

    >>> exit
    exits the sms process

    >>> undo <number=1>
    reverse the last command or last <number> of commands

See each commands individual docstring for return details.
"""
from cli_errors import RunnerError
from somewhatDb_database import db
from stack import EmptyStackError


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
        raise SystemExit

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

        # Try to typecast the "actions" to an integer: by default this will
        # be a string. If we get an error during the process,
        # it's not an integer!
        try:
            actions = int(actions)
        except ValueError:
            raise_number_error()

        # If the number is less than one, we should raise an error.
        if actions < 1:
            raise_number_error()

        # Otherwise, undo the number of commands requested, or until we get
        # an EmptyStackError.
        try:
            for x in range(actions):
                db.undo()
        except EmptyStackError:
            raise RunnerError('No commands to undo.')
