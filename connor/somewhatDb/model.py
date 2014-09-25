from .database import db


class Model:

    def __init__(self, attributes={}):
        self.iid = attributes['iid'] if 'iid' in attributes else None

        self._attributes = attributes

    @classmethod
    def db(cls):
        """ (Model) -> Database
        Returns the database collection for the model.
        """
        return getattr(db, cls.__name__)

    @classmethod
    def find(cls, attrs):
        """ (Model, string|dict) -> []Model
        Attempts to find models by the given parameter. Returns a
        list of models. See #database.find for use.
        """
        return [cls(data) for data in cls.db().find(attrs, True)]

    @classmethod
    def find_one(cls, attr):
        """ (Model, string|dict) -> Model
        Attempts to find a single model by the given parameters.
        Returns none, or the model. See #database.find_one for use.
        """
        result = cls.db().find_one(attr, True)

        if result is not None:
            return cls(result)

        return None

    def save(self):
        """ (Model) -> NoneType
        Persists the model. Creates it if it does not exist
        """
        if self.iid is not None:
            self.db().update(self.iid, self._attributes)
        else:
            self.iid = self.db().add(self._attributes)

    def delete(self):
        """ (Model) -> NoneType
        Removes the model from the collection, if it has been saved.
        """
        if self.iid is not None:
            self.db().remove(self.iid)

    def set(self, key, value):
        """ (Model, string, object) -> NoneType
        Resolves missing attribute assignments to use the
        model's "attributes" dict, which is pulled from the db.
        """
        self._attributes[key] = value

    def get_id(self):
        """ (Model) -> string
        Gets this models' ID.
        """
        return self.iid

    def get(self, item):
        """ (Model, string) -> object
        Resolves missing attributes to use the model's
        "attributes" dict, which is pulled from the db.
        """
        return self._attributes[item]
