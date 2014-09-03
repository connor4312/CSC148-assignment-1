from .transactor import Transactor
import uuid
import copy


class Database(Transactor):

    def __init__(self):
        Transactor.__init__(self)

        self.data = {}
        self.collection_key = None
        self.current_collection = None

    def _dict_matches(self, compare, against):
        """
        Checks to see if all the values in "against" are in the comare
        and that they are equal.
        """
        for key, value in against.items():
            if not key in compare or compare[key] != value:
                return False

        return True

    def _find_ids(self, attr):
        """
        Attempts to find the given item in the collection. If attr is a
        string, assume it's a UUID. Otherwise, match it against a dict.
        The record must match everything given in the dict. Returns an
        array of object ids (strings).
        """

        # If we're being given a string, assume it's a UUID
        if isinstance(attr, str):
            if attr in self.current_collection:
                return [attr]

            return []

        # Otherwise, it's a dict to match!
        out = []
        for id, item in self.current_collection.items():
            if self._dict_matches(item, attr):
                out.append(id)

        return out

    def _get_record_for(self, id):
        return self.current_collection[id]

    def set_collection(self, name):
        """
        Sets a collection from the "database", creating one if it
        does not already exist.
        """
        if not name in self.data:
            self.data[name] = {}

        self.collection_key = name
        self.current_collection = self.data[name]

        return self

    def add(self, data=None, id=None, **kwargs):
        """
        Adds an item to the collection. Takes a dict to add, an array
        of dicts, to add, or data as keyword arguments. Returns an
        array of added IDs.
        """
        # If it's a list of multiple items, add them individually.
        if isinstance(data, list):
            return [self.add(d) for d in data]

        # Generate a UUID
        if id is None:
            id = uuid.uuid4().hex

        # Add the keyword args or data, depending on which we're using.
        if data is None:
            self.current_collection[id].append(kwargs)
        else:
            # Copy the data to prevent strange reference issues...
            self.current_collection[id] = copy.copy(data)

        # Add an undo action
        key = self.collection_key
        self.add_action(lambda: self.set_collection(key).remove(id))

        return id

    def remove(self, attr):
        """
        Removes an item by ID/attribute from the current collection. See
        find() for usage.
        """

        recs = []
        for id in self._find_ids(attr):
            keep = self.current_collection[id]
            self.add_action(lambda id=id, keep=keep: self.set_collection(key).add(keep, id))

            recs.append(keep)

            del self.current_collection[id]

        key = self.collection_key

    def update(self, id, data=None, **kwargs):
        """
        Updates an existing item. Returns false if the record didn't exist,
        true otherwise.
        """
        if id not in self.current_collection:
            return False

        record = self.current_collection[id]

        # Save the current collection to "reverse"
        key = self.collection_key
        record_copy = copy.copy(record)
        self.add_action(lambda: self.set_collection(key).update(id, record_copy))

        # If the data is none, assume we're being given keyworded arguments
        if data is None:
            record.update(kwargs)
        # Otherwise, update with the data (which we assume is a dict)
        else:
            record.update(data)

        return True

    def find(self, attr):
        """
        Attempts to find the given item in the collection. If attr is a
        string, assume it's a UUID. Otherwise, match it against a dict.
        The record must match everything given in the dict. Example:

            db.students.find({"name": "Connor"})

        Returns an array of dicts.
        """

        return map(self._get_record_for, self._find_ids(attr))

    def find_one(self, attr):
        """
        Same as "find", but returns a single dict or false, rather
        than an array.
        """
        data = self._find_ids(attr)

        return False if not len(data) else self.current_collection[data[0]]

    def __getattr__(self, name):
        """
        Allow pymongo-style collection names. For instance:

            db.someCollection.find(42)

        Returns the current object.
        """
        self.set_collection(name)

        return self