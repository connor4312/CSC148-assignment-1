"""
Represents a many-to-many relationship between a parent instance and a child
class. It uses a SQL-style pivot table to link the relations. Usage in
model initializations:

    self.others = ManyToMany(self, OtherModel)

We can then conveniently attach and detach OtherModels to the instance.
These relations are contained in the pivot table, meaning that they are
shared between the "parent" and "child" automatically.

    model.others.attach(some_instance)
    model.others.find() # returns [some_instance]
    some_instance.models.find() # returns [model]

    some_other_instance.models.detach(model)
    model.others.find() # returns []
    some_instance.models.find() # returns []

"""
from somewhatDb_database import db


class ManyToMany:
    def __init__(self, parent, child):
        names = parent.__class__.__name__, child.__name__

        # If there's already been the complement of this relation
        # defined, we should try to use that first.
        if db.has_collection('_'.join(names)):
            self.name = '_'.join(names)
        else:
            self.name = '_'.join(reversed(names))
        # Then set the collection to ensure it's created!
        db.set_collection(self.name)

        self.parent = parent
        self.child = child

    def db(self):
        """ (ManyToMany) -> Database
        Gets the database connection for the relation.
        """
        return getattr(db, self.name)

    def _get_relation(self, model):
        """ (ManyToMany, Model) -> dict
        Creates a dict linking the parent model to the child.
        """

        return {
            self.parent.__class__.__name__: self.parent.get_id(),
            self.child.__name__: model.get_id()
        }

    def attach(self, model):
        """ (ManyToMany, Model) -> NoneType
        Attaches the model to this instance's subject.
        """
        if model.get_id() is None:
            model.save()

        self.db().crupdate(self._get_relation(model))

    def detach(self, model):
        """ (ManyToMany, Model) -> NoneType
        Detaches the model to this instance's subject.
        """
        if model.get_id() is None:
            return

        self.db().remove(self._get_relation(model))

    def find(self):
        """ (ManyToMany) -> []Model
        Finds all owned relations.
        """
        out = []
        attr = {self.parent.__class__.__name__: self.parent.get_id()}
        for record in self.db().find(attr):
            out.append(self.child.find_one(record[self.child.__name__]))

        return out
