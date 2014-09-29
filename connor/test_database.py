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
from somewhatDb_database import Database


class DatabaseTestCase(unittest.TestCase): # pragma: no cover

    def setUp(self):
        self.db = Database()

    def test_adds_and_finds_id(self):
        item = {'bar': True}

        self.db.start_transaction()
        id = self.db.foos.add({'bar': True})
        self.assertEqual(item, self.db.foos.find_one(id))
        self.assertEqual(id, self.db.foos.find_one(id, include_id=True)['id'])
        self.db.end_transaction()

        self.assertEqual(False, self.db.foos.find_one(id))

    def test_adds_multiple(self):
        ids = self.db.foos.add([{'bar': True}, {'bar': False}])
        self.assertEqual(2, len(ids))

    def test_adds_kwargs(self):
        id = self.db.foos.add(bar=True)
        self.assertEqual({'bar': True}, self.db.foos.find_one(id))

    def test_finds_against_dict(self):
        item = {'bar': True}
        self.db.foos.add({'asdfdsf': 'asdfdsfs'})
        self.db.foos.add({'bar': False})
        self.db.foos.add(item)

        self.assertEqual(item, self.db.foos.find_one({'bar': True}))

    def test_adds_and_finds_id(self):
        item = {'bar': True}
        id = self.db.foos.add(item)

        self.assertEqual(item, self.db.foos.find_one(id))

    def test_deletes(self):
        id = self.db.foos.add({'bar': True})

        self.db.start_transaction()
        self.db.foos.remove(id)
        self.assertEqual(None, self.db.foos.find_one(id))
        self.db.end_transaction()

        self.db.undo()
        self.assertNotEqual(None, self.db.foos.find_one(id))

    def test_updates(self):
        id = self.db.foos.add({'bar': True})
        self.assertEqual(False, self.db.foos.update('foo', {}))

        self.db.start_transaction()
        self.db.foos.update(id, {'bar': False})
        self.assertEqual(False, self.db.foos.find_one(id)['bar'])
        self.db.foos.update(id, bar='blarg')
        self.assertEqual('blarg', self.db.foos.find_one(id)['bar'])
        self.db.end_transaction()

        self.db.undo()
        self.assertEqual(True, self.db.foos.find_one(id)['bar'])

    def test_crupdates(self):
        id = self.db.foos.crupdate({'bar': True})
        self.assertEqual({'bar': True}, self.db.foos.find_one(id))
        self.db.foos.crupdate({'bar': True}, {'baz': 42})
        self.assertEqual({'bar': True, 'baz': 42}, self.db.foos.find_one(id))
