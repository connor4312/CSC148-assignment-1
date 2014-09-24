from .database import db


class Model:

    def __init__(self, attributes={}):
        self.iid = attributes['iid'] if 'iid' in attributes else None

        self._attributes = attributes
        self._relations = self.get_relations()

    def get_relations(self):
        """
        Returns a list of model relations.
        """
        return []

    @classmethod
    def db(cls):
        """
        Returns the database collection for the model.
        """
        return getattr(db, cls.__name__)

    @classmethod
    def find(cls, attrs):
        """
        Attempts to find models by the given parameter. Returns a
        list of models. See #database.find for use.
        """
        return [cls(data) for data in cls.db().find(attrs, True)]

    @classmethod
    def find_one(cls, attr):
        """
        Attempts to find a single model by the given parameters.
        Returns none, or the model. See #database.find_one for use.
        """
        result = cls.db().find_one(attr, True)

        if result is not None:
            return cls(result)

        return None

    def save(self):
        """
        Persists the model. Creates it if it does not exist
        """
        if self.iid is not None:
            self.db().update(self.iid, self._attributes)
        else:
            self.iid = self.db().add(self._attributes)

    def delete(self):
        """
        Removes the model from the collection, if it has been saved.
        """
        if self.iid is not None:
            self.db().remove(self.iid)

    def set(self, key, value):
        """
        Resolves missing attribute assignments to use the
        model's "attributes" dict, which is pulled from the db.
        """
        self._attributes[key] = value

    def get_id(self):
        return self.iid

    def get(self, item):
        """
        Resolves missing attributes to use the model's
        "attributes" dict, which is pulled from the db.
        """
        return self._attributes[item]
