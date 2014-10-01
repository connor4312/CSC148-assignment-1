"""
The Database is the persistence layer which powers the application. It stores
data in dicts (like NoSQL collections), and gives every row a numeric ID for
reference. It extends the Transactor, so any action taken can be rolled back
easily.

See individual method documentation for further usage.
"""
from somewhatDb_transactor import Transactor


def dict_matches(compare, against):
    """ (dict, dict) -> boolean
    Checks to see if all the values in "against" are in the compare,
    and that they are equal.
    """
    for key, value in against.items():
        if key not in compare or compare[key] != value:
            return False

    return True


def copy(dictionary):
    """ (dict) -> dict
    Performs a manual deep-copy of a dict. Normally we'd use the copy module,
    but we can't import that!
    """
    output = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            output[key] = copy(value)
        else:
            output[key] = value

    return output


class Database(Transactor):

    def __init__(self):
        Transactor.__init__(self)

        self.data = {}
        self.collection_key = None
        self.current_collection = None
        self.id_increment = 0

    def _find_ids(self, attr):
        """ (Database, string|dict) -> []string
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
        for iid, item in self.current_collection.items():
            if dict_matches(item, attr):
                out.append(iid)

        return out

    def _get_record_for(self, iid, include_id):
        """ (Database, string, boolean) -> dict
        Looks up a record by its ID. If include_id is true, then we'll include
        the id itself in an "iid" property of the dict.
        """
        record = copy(self.current_collection[iid])

        if include_id:
            record['iid'] = iid

        return record

    def has_collection(self, name):
        """ (Database, string) -> boolean
        Returns whether or not the given collection yet exists.
        """
        return name in self.data

    def set_collection(self, name):
        """ (Database, name) -> Database
        Sets a collection from the "database", creating one if it
        does not already exist.
        """
        if not self.has_collection(name):
            self.data[name] = {}

        self.collection_key = name
        self.current_collection = self.data[name]

        return self

    def add(self, data=None, iid=None, **kwargs):
        """ (Database, dict|[]dict, string) -> string
        Adds an item to the collection. Takes a dict to add, an array
        of dicts, to add, or data as keyword arguments. Returns an
        array of added IDs.
        """
        # If it's a list of multiple items, add them individually.
        if isinstance(data, list):
            return [self.add(d) for d in data]

        # Generate a UUID
        if iid is None:
            iid = '%s' % self.id_increment
            self.id_increment += 1

        # Add the keyword args or data, depending on which we're using.
        if data is None:
            self.current_collection[iid] = kwargs
        else:
            # Copy the data to prevent strange reference issues...
            self.current_collection[iid] = copy(data)

        # Add an undo action
        key = self.collection_key
        self.add_action(lambda: self.set_collection(key).remove(iid))

        return iid

    def remove(self, attr):
        """ (Database, string|dict) -> NoneType
        Removes an item by ID/attribute from the current collection. See
        find() for usage.
        """

        recs = []
        for iid in self._find_ids(attr):
            keep = self.current_collection[iid]
            self.add_action(lambda iid=iid, keep=keep: self
                            .set_collection(key).add(keep, iid))

            recs.append(keep)

            del self.current_collection[iid]

        key = self.collection_key

    def update(self, iid, data=None, **kwargs):
        """ (Database, string, dict) -> boolean
        Updates an existing item. Returns false if the record didn't exist,
        true otherwise.
        """
        if iid not in self.current_collection:
            return False

        record = self.current_collection[iid]

        # Save the current collection to "reverse"
        key = self.collection_key
        record_copy = copy(record)
        self.add_action(lambda: self.set_collection(key)
                                    .update(iid, record_copy))

        # If the data is none, assume we're being given keyworded arguments
        if data is None:
            record.update(kwargs)
        # Otherwise, update with the data (which we assume is a dict)
        else:
            record.update(data)

        return True

    def crupdate(self, attr, data=None):
        """ (Database, string|dict, dict) -> string
        If a model with the given attr rules (see find()) is in the collection
        then update it. Otherwise, create it.
        """
        if data is None:
            data = attr

        records = self._find_ids(attr)
        if len(records) == 0:
            return self.add(data)

        self.update(records[0], data)

        return records[0]

    def find(self, attr={}, include_id=False):
        """ (Database, string|dict, boolean) -> []dict
        Attempts to find the given item in the collection. If attr is a
        string, assume it's a UUID. Otherwise, match it against a dict.
        The record must match everything given in the dict. Example:

            db.students.find({"name": "Connor"})

        Returns an array of dicts.
        """
        return map(lambda r: self._get_record_for(r, include_id),
                   self._find_ids(attr))

    def find_one(self, attr, include_id=False):
        """ (Database, string|dict, boolean) -> dict
        Same as "find", but returns a single dict or None, rather
        than an array.
        """
        data = self._find_ids(attr)

        if not len(data):
            return None

        return self._get_record_for(data.pop(), include_id)

    def __getattr__(self, name):
        """ (Database, string) -> object
        Allow pymongo-style collection names. For instance:

            db.someCollection.find(42)

        Returns the current object.
        """
        self.set_collection(name)

        return self

db = Database()
