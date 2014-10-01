"""
Management for a transaction. This is a layer on top of the normal stack ADT,
and it does interact with the stack using only push(), pop(), and is_empty().
Its responsiblity is to decorate the stack to allow grouping of multiple events
and undo functionality, for the database to consume.
"""
from stack import Stack


class Transactor:

    def __init__(self):
        self.stack = Stack()
        self.transaction_queue = []

    def start_transaction(self):
        """ (Transactor) -> NoneType
        Starts an "undo"-able set of events.
        """
        self.transaction_queue = []

    def end_transaction(self):
        """ (Transactor) -> NoneType
        Ends the current set of events.
        """
        self.stack.push(self.transaction_queue)
        self.transaction_queue = []

    def add_action(self, action):
        """ (Transactor, function) -> NoneType
        Adds an action onto the list of transactions.
        """
        self.transaction_queue.append(action)

    def undo(self):
        """ (Transactor) -> NoneType
        Undoes the last set of transactions. Returns true on success, or
        false on failure (indicating there were no more transactions to undo).
        Can throw a stack.EmptyStackError, which should be handled!
        """
        for cmd in reversed(self.stack.pop()):
            cmd()
