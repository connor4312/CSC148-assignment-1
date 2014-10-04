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

        runner.resolve_command('create student connor')
        runner.resolve_command('create student george')
        runner.resolve_command('create student anish')

    def test_missing_command(self):
        self.assertEqual(runner.resolve_command(
            'lalalala'), 'Unrecognized command!')

    def test_handles_multiple_spaces(self):
        self.assertEqual(runner.resolve_command(
            'create     student     david'), None)
        self.assertEqual(runner.resolve_command(
            'create student david'), 'ERROR: Student david already exists.')

    def test_creates_student(self):
        self.assertEqual(runner.resolve_command(
            'create student david'), None)
        self.assertEqual(runner.resolve_command(
            'create student david'), 'ERROR: Student david already exists.')

    def test_lists_courses_no_student(self):
        self.assertEqual(runner.resolve_command(
            'list-courses foo'), 'ERROR: Student foo does not exist.')

    def test_list_courses_no_courses(self):
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_lists_courses_one_course(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking CSC148')

    def test_lists_courses_sorts(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor Z'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking A, CSC148, Z')

    def test_enrols_student_no_exist(self):
        self.assertEqual(runner.resolve_command(
            'enrol foo CSC148'), 'ERROR: Student foo does not exist.')

    def test_enrols_student(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking CSC148')

    def test_enrol_duplicate_does_nothing(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking A')
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking A')
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_enrols_stops_at_30(self):
        for i in range(30):
            self.assertEqual(runner.resolve_command(
                'create student foo%s' % i), None)
            self.assertEqual(runner.resolve_command(
                'enrol foo%s CSC148' % i), None)

        self.assertEqual(runner.resolve_command(
            'create student foo30'), None)
        self.assertEqual(runner.resolve_command(
            'enrol foo30 CSC148'), 'ERROR: Course CSC148 is full.')
        self.assertEqual(runner.resolve_command(
            'enrol foo29 CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses foo30'), 'foo30 is not taking any courses.')
        self.assertEqual(runner.resolve_command(
            'list-courses foo29'), 'foo29 is taking CSC148')

    def test_drops_student_no_exist(self):
        self.assertEqual(runner.resolve_command(
            'drop foo CSC148'), 'ERROR: Student foo does not exist.')

    def test_drops_from_nonexist(self):
        self.assertEqual(runner.resolve_command(
            'drop connor CSC148'), None)

    def test_drops_student_from_course(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'drop connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_common_courses_no_exist(self):
        self.assertEqual(runner.resolve_command(
            'common-courses connor baz'), 'ERROR: Student baz does not exist.')

        self.assertEqual(runner.resolve_command(
            'common-courses nil baz'),
            'ERROR: Student nil does not exist.\n' +
            'ERROR: Student baz does not exist.')
        # Make sure it's in the right order!
        self.assertEqual(runner.resolve_command(
            'common-courses baz nil'),
            'ERROR: Student baz does not exist.\n' +
            'ERROR: Student nil does not exist.')

    def test_common_courses_empty(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC165'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses connor george'), '')

    def test_common_courses_multiple(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC165'), None)
        self.assertEqual(runner.resolve_command(
            'enrol george CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses connor george'), 'CSC148')
        self.assertEqual(runner.resolve_command(
            'enrol george A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol george Z'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor Z'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses connor george'), 'A, CSC148, Z')

    def test_class_list_none(self):
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'No one is taking CSC148.')

    def test_class_list_single(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'connor')

    def test_class_list_multiple(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'enrol george CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'enrol anish CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'anish, connor, george')
        self.assertEqual(runner.resolve_command(
            'drop connor CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'drop george CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'drop anish CSC148'), None)
        self.assertEqual(runner.resolve_command(
            'class-list CSC148'), 'No one is taking CSC148.')

    def test_undos_none(self):
        # undo the setup stuff
        self.assertEqual(runner.resolve_command(
            'undo 3'), None)

        self.assertEqual(runner.resolve_command(
            'undo'), 'ERROR: No commands to undo.')

    def test_undos_bad_input(self):
        self.assertEqual(runner.resolve_command(
            'undo a'), 'ERROR: a is not a positive natural number.')
        self.assertEqual(runner.resolve_command(
            'undo -1'), 'ERROR: -1 is not a positive natural number.')

    def test_undos_create_student(self):
        self.assertEqual(runner.resolve_command(
            'create student foo'), None)
        self.assertEqual(runner.resolve_command(
            'create student foo'), 'ERROR: Student foo already exists.')
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'create student foo'), 'ERROR: Student foo already exists.')
        self.assertEqual(runner.resolve_command(
            'undo 2'), None)
        self.assertEqual(runner.resolve_command(
            'create student foo'), None)

    def test_undos_enrol_student(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor B'), None)
        self.assertEqual(runner.resolve_command(
            'undo 2'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_undos_multiple_times(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'enrol connor B'), None)
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_undos_drop_courses(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'drop connor A'), None)
        self.assertEqual(runner.resolve_command(
            'undo 2'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_undos_works_with_list(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is taking A')
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_undos_works_with_common_courses(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'common-courses connor anish'), '')
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_undos_works_with_class_list(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'class-list A'), 'connor')
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_undos_works_with_unrecognized(self):
        self.assertEqual(runner.resolve_command(
            'enrol connor A'), None)
        self.assertEqual(runner.resolve_command(
            'lalalala'), 'Unrecognized command!')
        self.assertEqual(runner.resolve_command(
            'undo'), None)
        self.assertEqual(runner.resolve_command(
            'list-courses connor'), 'connor is not taking any courses.')

    def test_exits(self):
        with self.assertRaises(SystemExit):
            runner.resolve_command('exit')
