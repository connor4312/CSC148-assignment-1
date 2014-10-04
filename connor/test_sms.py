"""
This TestCase is effectively a set of e2e functional tests for the entire
application, ensuring that it (hopefully!) operates flawlessly based on the
requirements of the assignment.
"""
import unittest
from sms import runner
from somewhatDb_database import db
from stack import Stack


class SmsTestCase(unittest.TestCase):

    def setUp(self):
        db.data = {}
        db.stack = Stack()

    def test_missing_command(self):
        self.assertEqual(runner.resolve_command(
            'foo'), 'ERROR: Command not found')

    def test_creates_student(self):
        self.assertEqual(runner.resolve_command(
            'create student david'), None)
        self.assertEqual(runner.resolve_command(
            'create student david'), 'ERROR: Student david already exists.')

    def tests_lists_courses(self):
        self.assertEqual(runner.resolve_command(
            'create student connor'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking CSC148')
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor Z'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking A, CSC148, Z')
        self.assertEqual(runner.resolve_command(
            'list-courses foo'), 'ERROR: Student foo does not exist.')

    def test_enrols_student(self):
        self.assertEqual(runner.resolve_command(
            'enrol foo CSC148'), 'ERROR: Student foo does not exist.')

        for i in range(30):
            self.assertEqual(runner.resolve_command(
                'create student connor%s' % i), None)
            self.assertEqual(runner.resolve_command(
                'enrol connor%s CSC148' % i), None)

        self.assertEqual(runner.resolve_command(
            'create student connor30'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor30 CSC148'), 'ERROR: Course CSC148 is full.')
        self.assertEqual(runner.resolve_command(
            'list-courses connor30'), 'connor30 is not taking any courses.')
        self.assertEqual(runner.resolve_command(
            'list-courses connor29'), 'connor29 is taking CSC148')

    def test_drops_student(self):
        self.assertEqual(runner.resolve_command(
            'drop foo CSC148'), 'ERROR: Student foo does not exist.')
        self.assertEqual(runner.resolve_command(
            'create student connor'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'drop connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_common_courses(self):
        self.assertEqual(runner.resolve_command(
            'create student foo'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'create student bar'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses foo bar'), '')
        self.assertEqual(runner.resolve_command(
            'common-courses foo baz'), 'ERROR: Student baz does not exist.')
        self.assertEqual(runner.resolve_command(
            'common-courses nil baz'),
            'ERROR: Student nil does not exist.\n' +
            'ERROR: Student baz does not exist.')

        self.assertEqual(runner.resolve_command(
            'enrol bar CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses foo bar'), 'CSC148')
        self.assertEqual(runner.resolve_command(
            'enrol bar A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol bar Z'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo Z'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses foo bar'), 'A, CSC148, Z')

    def test_class_list(self):
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'No one is taking CSC148.')
        self.assertEqual(runner.resolve_command(
            'create student foo'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'foo')
        self.assertEqual(runner.resolve_command(
            'drop foo CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'No one is taking CSC148.')

    def test_undos(self):
        self.assertEqual(runner.resolve_command(
            'undo'), 'ERROR: No commands to undo.')
        self.assertEqual(runner.resolve_command(
            'undo a'), 'ERROR: a is not a positive natural number.')
        self.assertEqual(runner.resolve_command(
            'undo -1'), 'ERROR: -1 is not a positive natural number.')
        self.assertEqual(runner.resolve_command(
            'create student foo'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo B'), None)
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses foo'), 'foo is not taking any courses.')
        self.assertEqual(runner.resolve_command(
            'enrol foo B'), None)
        self.assertEqual(runner.resolve_command(
            'undo 2'), None)
        self.assertEqual(runner.resolve_command(
            'create student foo'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo A'), None)
        self.assertEqual(runner.resolve_command(
            'drop foo A'), None)
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses foo'), 'foo is taking A')

    def test_exits(self):
        with self.assertRaises(SystemExit):
            runner.resolve_command('exit')
