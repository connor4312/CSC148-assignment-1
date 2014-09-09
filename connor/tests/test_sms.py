# Assignment 1 - Sample unit tests
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sample unit tests for sms.py.

Because we're the code we're testing interacts
with the console, we need to do a bit of fiddling
to handle standard input and output.
Luckily for you, we've provided a base method
that does all of the work; you just need to provide
the actual test cases.
"""
import unittest
import sys
from io import StringIO
from sms import runner


class SmsTestCase(unittest.TestCase):

    # Methods for redirecting input and output
    # Do not change these!
    def setUp(self):
        self.out = StringIO('')
        sys.stdout = self.out

    def tearDown(self):
        self.out.close()
        self.out = None
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    def assert_io(self, commands, outputs):
        """ (list of str, list of str) -> NoneType

        Simulate running input sms commands,
        check whether the output corresponds to outputs.
        DO NOT CHANGE THIS METHOD!

        Name was changed for compatiblity with nose/py3.4.
        Was attempting to run io_tester, because test was
        in its name.
        """
        sys.stdin = StringIO('\n'.join(commands))
        runner.run()
        self.assertEqual(self.out.getvalue(), '\n'.join(outputs))

    def test_simple(self):
        with self.assertRaises(SystemExit) as c:
            self.assert_io(['exit'], [''])

    def test_duplicate_student(self):
        with self.assertRaises(SystemExit) as c:
            self.assert_io(['create student david', 'create student david', 'exit'],
                           ['ERROR: Student david already exists.', ''])