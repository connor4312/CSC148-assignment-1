from somewhatDb_database import db
from cli_errors import RunnerError


class Runner():

    def __init__(self):
        self.commands = {}

    def _wrap_transact(self, func):
        """ (Runner, function) -> function
        Wraps a function so that a transaction is started
        and ended "around" it.
        """
        def transacted(*args, **kwargs):
            db.start_transaction()
            output = func(*args, **kwargs)
            db.end_transaction()
            return output

        return transacted

    def _build_command(self, prefix, transact, func):
        """ (Runner, string, boolean, function) -> function
        Add the command to our dict, ready to call! Then, just return it.
        We don't really care about *actually* decorating the method here.
        Just giving some syntactic sugar instead of a huge if/else or
        a bunch of annoying lambdas.
        """

        if transact:
            func = self._wrap_transact(func)

        self.commands[prefix] = func

        return func

    def resolve_command(self, input):
        """ (Runner, string) -> string|NoneType
        Takes an input string, from the CLI, and attempts to resolve the
        command it matches up to. If a function is found, it is called.
        Otherwise, None is returned.
        """
        for command, func in self.commands.items():
            if input.startswith(command):
                args = input.replace(command, '').strip().split()

                try:
                    return func(*args)
                except RunnerError as e:
                    return 'ERROR: ' + str(e)

        return None

    def command(self, prefix, transact=False):
        """ (Runner, string, boolean) -> function
        Simple method to be used as a decorator, which returns a function
        to build a command. Takes a string prefix as its only argument. Use:

            @runner.command("is this")
            def college_check(college):
                print('Yes!') if college == 'Toronto' else print ('No!')

        The function can then be called on the command line in the format
        `is this <college>`.
        """

        return lambda func: self._build_command(prefix, transact, func)

    def run(self):
        """ (Runner) -> NoneType
        Loop to run the CLI input parser.
        """

        while True:
            output = self.resolve_command(input('').strip())

            if output is None:
                print('Unrecognized command!')
            else:
                print(output)
