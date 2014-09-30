"""
This module's "link" function binds the student enrolment commands to the test
runner. By invoking link(Runner), the following commands become available:

    >>> create student <student>
    create a new student with <student>

    >>> enrol <student> <course>
    enrol student <student> into <course>

    >>> drop <student> <name>
    remove <student> from <course>

    >>> list-courses <student>
    print a list of codes of all the course taken by <student>

    >>> class-list <course>
    print a list of all students enrolled in <course>

    >>> common-courses <student1> <student2> <student3> ...
    print a list of all courses taken by the given students

See each commands individual docstring for return details.
"""

from cli_errors import RunnerError
from somewhatDb_models_student import Student
from somewhatDb_models_course import Course

MAX_STUDENTS_PER_COURSE = 30


def link(runner):
    """ (Runner) -> NoneType
    Binds enrolment commands to the task runner.
    """

    @runner.command('create student', transact=True)
    def create_student(name):
        """ (string) -> string
        Attempts to create a student with the given name. Example usage:

            > create student david

        An error will be raised if the student already exists.
        """

        if Student.find_one({'name': name}) is not None:
            raise RunnerError('Student %s already exists.' % name)

        student = Student()
        student.set('name', name)
        student.save()

        return ''

    @runner.command('enrol', transact=True)
    def enrol_student(name, course_name):
        """ (string, string) -> string
        Enrols the student in the given course. Example usage:

            > enrol david CSC148

        The course will be created if it does not exist, and an error will
        be raised if the course is full or the student doesn't exist.
        """

        student = Student.find_one({'name': name})
        if student is None:
            raise RunnerError('Student %s does not exist.' % name)

        course = Course.find_one({'name': course_name})
        if course is None:
            course = Course()
            course.set('name', course_name)
            course.save()

        if len(course.students.find()) >= MAX_STUDENTS_PER_COURSE:
            raise RunnerError('Course %s is full.' % course_name)

        student.courses.attach(course)

        return ''

    @runner.command('drop', transact=True)
    def drop_course(name, course_name):
        """ (string, string) -> string
        Removes a student from the course, if they are enroled in it. Example
        usage:

            > drop bob CSC148

        An error will be raised if the student doesn't exist.
        """

        student = Student.find_one({'name': name})
        if student is None:
            raise RunnerError('Student %s does not exist.' % name)

        course = Course.find_one({'name': course_name})
        if course is not None:
            student.courses.detach(course)

        return ''

    @runner.command('list-courses')
    def list_courses(name):
        """ (string) -> string
        List the courses taken by a student. Example usage:

            > list-courses david

        An error will be raised if the student doesn't exist.
        """

        student = Student.find_one({'name': name})
        if student is None:
            raise RunnerError('Student %s does not exist.' % name)

        courses = sorted([c.get('name') for c in student.courses.find()])
        if len(courses) == 0:
            return '%s is not taking any courses.' % name

        return '%s is taking %s' % (name, ', '.join(courses))

    @runner.command('class-list')
    def class_list(name):
        """ (string) -> string
        Lists students in a given course. Example usage:

            > class-list CSC148

        Returns a comma-delimited string of courses, or notifies that no one
        is taking that particular course.
        """

        course = Course.find_one({'name': name})
        if course is None:
            return 'No one is taking %s.' % name

        students = [c.get('name') for c in course.students.find()]
        if len(students) == 0:
            return 'No one is taking %s.' % name

        return ', '.join(students)

    @runner.command('common-courses')
    def common_courses(*students):
        """ ([]string) -> string
        Lists the courses the given set of students has in common.
        Example usage:

            > common-courses george connor

        It raises an error if any of the students don't exist.
        """

        course_sets = []
        error = []
        for name in students:
            record = Student.find_one({'name': name})
            if record is None:
                error.append('ERROR: Student %s does not exist.' % name)
            else:
                names = [c.get('name') for c in record.courses.find()]
                course_sets.append(names)

        if len(error):
            return '\n'.join(error)

        common_set = set(course_sets[0])
        for course_set in course_sets[1:]:
            common_set = common_set.intersection(set(course_set))

        return ', '.join(sorted(list(common_set)))
