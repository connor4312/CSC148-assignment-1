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
