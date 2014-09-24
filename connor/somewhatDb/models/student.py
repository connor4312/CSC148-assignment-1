from ..model import Model
from ..associations import ManyToMany


class Student(Model):
    def __init__(self, *args):
        super().__init__(*args)

        # The import is done here to prevent a circular dependency
        from .course import Course
        self.courses = ManyToMany(self, Course)
