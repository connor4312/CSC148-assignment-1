from ..model import Model
from ..associations import ManyToMany


class Course(Model):
    def __init__(self, *args):
        super().__init__(*args)

        # The import is done here to prevent a circular dependency
        from .student import Student
        self.students = ManyToMany(self, Student)