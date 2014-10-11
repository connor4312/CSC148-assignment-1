from somewhatDb_database import db
from cli_errors import RunnerError, RunnerHalterError


class Runner():

    def __init__(self):
        self.commands = {}

    def _wrap_transact(self, func):
        """ (Runner, function) -> function
        Wraps a function so that a transaction is started and ended "around"
        it. We handle two exceptions: RunnerError and RunnerHalterError.
        """
        def transacted(*args, **kwargs):
            db.start_transaction()

            try:
                # Try to get the output from the function...
                output = func(*args, **kwargs)
            except RunnerHalterError as e:
                # On a halter error, re-raise it but do NOT close
                # the transaction.
                raise e
            except RunnerError as e:
                # On a runner error, end the transaction before raising the
                # error again to handle it at a higher level.
                db.end_transaction()
                raise e

            # If we're all good, end the transaction and return the output!
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

        # Normally I'd use regex for this, but we can't import re :(
        input = ' '.join(input.split())

        # Given an input, look through every command...
        for command, func in self.commands.items():
            # If the input starts with our lovely command
            if input.startswith(command):
                # Remove the command part, strip any spaces, and split
                # the "words" which we'll use as arguments.
                args = input.replace(command, '').strip().split()

                try:
                    # Pass the words in as positional arguments to the
                    # bound function.
                    return func(*args)
                except RunnerError as e:
                    # If we got an error and it has a message, print it...
                    if len(str(e)):
                        return 'ERROR: ' + str(e)

                    # If it doesn't have an error, return none
                    return None

        # At this point, if the command is valid it will have returned
        # something. If it's an invalid command, we still want to push
        # a transaction, so do that now...
        db.start_transaction()
        db.end_transaction()

        # And return unknown command
        return 'Unrecognized command!'

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
