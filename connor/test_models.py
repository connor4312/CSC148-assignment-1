"""
This TestCase tests the somewhatDb_model.Model and the Many to Many
relationship, using the Course and Student and fixtures.
"""
import unittest
from somewhatDb_models_course import Course
from somewhatDb_models_student import Student


class ModelsTestCase(unittest.TestCase): # pragma: no cover

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

        c.students.attach(s)
        self.assertEqual(s.get_id(), c.students.find()[0].get_id())

        c.students.detach(s)
        self.assertEqual(0, len(c.students.find()))
        c.students.detach(Student())
