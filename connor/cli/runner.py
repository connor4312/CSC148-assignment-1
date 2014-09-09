import re


class Runner():

    command_regexp = re.compile(r'<[a-z_]+>')

    def __init__(self):
        self.commands = {}

    def _build_command(self, prefix, func):
        """
        Add the command to our dict, ready to call! Then, just return it.
        We don't really care about *actually* decorating the method here.
        Just giving some syntactic sugar instead of a huge if/else or
        a bunch of annoying lambdas.
        """

        self.commands[prefix] = func

        return func

    def _resolve_command(self, input):
        """
        Takes an input string, from the CLI, and attempts to resolve the
        command it matches up to. If a function is found, it is called.
        Otherwise, None is returned.
        """
        for command, func in self.commands.items():
            if input.startswith(command):
                args = input.replace(command, '').strip().split()

                return func(*args)

        return None

    def command(self, prefix):
        """
        Simple method to be used as a decorator, which returns a function
        to build a command. Takes a string prefix as its only argument. Use:

            @runner.command("is this")
            def college_check(college):
                print('Yes!') if college == 'Toronto' else print ('No!')

        The function can then be called on the command line in the format
        `is this <college>`.
        """

        return lambda func: self._build_command(prefix, func)

    def run(self):
        """
        Loop to run the CLI input parser.
        """

        while True:
            output = self._resolve_command(input('').strip())

            if output is None:
                print('Unrecognized command!')
            else:
                print(output)