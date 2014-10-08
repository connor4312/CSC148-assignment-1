"""
Represents a course that students can take. Contains a many to many relation
for "students".
"""
from somewhatDb_model import Model
from somewhatDb_associations_manyToMany import ManyToMany


class Course(Model):
    def __init__(self, *args):
        super().__init__(*args)

        # The import is done here to prevent a circular dependency
        from somewhatDb_models_student import Student
        self.students = ManyToMany(self, Student)

    def name(self, new_name=None):
        """ (string|NoneType) -> string
        Gets the course name or, if passed, updates the course's name to the
        given name. We don't need to do any validation in this application but,
        were we to do so, that would be done here!
        """
        if new_name is not None:
            self.set('name', new_name)

        return self.get('name')
