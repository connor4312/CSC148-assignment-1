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
from somewhatDb.models.course import Course
from somewhatDb.models.student import Student


class ModelsTestCase(unittest.TestCase):

    def test_creates_finds(self):
        c = Course()
        c.set('foo', 'bar')
        c.save()

        self.assertNotEqual(None, c.get_id())

        o = Course.find_one(c.get_id())
        self.assertEqual(c.get_id(), o.get_id())
        self.assertEqual('bar', o.get('foo'))

    def test_finds_multiple(self):
        c = Course()
        c.set('foo', 'bar')
        c.save()

        self.assertNotEqual(None, c.get_id())

        o = Course.find(c.get_id())
        self.assertEqual(c.get_id(), o[0].get_id())

    def test_deletes(self):
        c = Course()
        c.set('foo', 'bar')
        c.save()
        c.delete()

        self.assertEqual(None, Course.find_one(c.get_id()))

    def test_edits(self):
        c = Course()
        c.set('this', 'wontbeedited')
        c.set('foo', 'bar')
        c.save()
        c.set('foo', 'baz')
        c.save()

        o = Course.find_one(c.get_id())
        self.assertEqual(c.get_id(), o.get_id())
        self.assertEqual('wontbeedited', o.get('this'))
        self.assertEqual('baz', o.get('foo'))

    def tests_many_to_many(self):
        c = Course()
        c.save()
        s = Student()
        s.save()

        c.students.attach(s)
        self.assertEqual(s.get_id(), c.students.find()[0].get_id())

        c.students.detach(s)
        self.assertEqual(0, len(c.students.find()))