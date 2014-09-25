class Transactor:

    def __init__(self):
        self.transactions = []
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
        self.transactions.append(self.transaction_queue)
        self.transaction_queue = []

    def fake_transaction(self):
        """ (Transactor) -> NoneType
        Creates a transaction which does nothing when undone.
        """
        self.transactions.append(None)

    def undo_count(self):
        """ (Transactor) -> NoneType
        Returns the total number of transactions which may be undone.
        """
        return len(self.transactions)

    def add_action(self, action):
        """ (Transactor, function) -> NoneType
        Adds an action onto the list of transactions.
        """
        self.transaction_queue.append(action)

    def undo(self):
        """ (Transactor) -> NoneType
        Undoes the last set of transactions. Returns true on success, or
        false on failure (indicating there were no more transactions to undo)
        """

        cmd = self.transactions.pop()
        while len(cmd) > 0:
            cmd.pop()()
