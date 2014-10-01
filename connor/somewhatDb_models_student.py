"""
Represents a student in the database. Contains a many to many relation
for "courses".
"""
from somewhatDb_model import Model
from somewhatDb_associations_manyToMany import ManyToMany


class Student(Model):
    def __init__(self, *args):
        super().__init__(*args)

        # The import is done here to prevent a circular dependency
        from somewhatDb_models_course import Course
        self.courses = ManyToMany(self, Course)

    def name(self, new_name=None):
        """ (string|NoneType) -> string
        Gets the student name or, if passed, updates the student's name to the
        given name. We don't need to do any validation in this application but,
        were we to do so, that would be done here!
        """
        if new_name is not None:
            self.set('name', new_name)

        return self.get('name')