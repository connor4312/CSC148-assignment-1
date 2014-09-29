from somewhatDb_model import Model
from somewhatDb_associations_manyToMany import ManyToMany


class Student(Model):
    def __init__(self, *args):
        super().__init__(*args)

        # The import is done here to prevent a circular dependency
        from somewhatDb_models_course import Course
        self.courses = ManyToMany(self, Course)
