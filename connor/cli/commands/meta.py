import sys
from cli.errors import RunnerError
from somewhatDb.database import db


def link(runner):
    """ (Runner) -> NoneType
    Binds "meta" commands to the task runner.
    """

    @runner.command('exit')
    def exit():
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

        def valueError():
            raise RunnerError('%s is not a positive natural number.' % actions)

        try:
            actions = int(actions)
        except ValueError:
            valueError()

        if actions < 0:
            valueError()

        if db.undo_count() < actions:
            raise RunnerError('No commands to undo.')

        for x in range(actions):
            db.undo()

        return ''
