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

        # If the student already exists, raise an error
        if Student.find_one({'name': name}) is not None:
            raise RunnerError('Student %s already exists.' % name)

        # Otherwise, create a new student and save it.
        student = Student()
        student.name(name)
        student.save()

    @runner.command('enrol', transact=True)
    def enrol_student(name, course_name):
        """ (string, string) -> string
        Enrols the student in the given course. Example usage:

            > enrol david CSC148

        The course will be created if it does not exist, and an error will
        be raised if the course is full or the student doesn't exist.
        """

        # Make sure the student already exists
        student = Student.find_one({'name': name})
        if student is None:
            raise RunnerError('Student %s does not exist.' % name)

        # If the course doesn't exist, create one.
        course = Course.find_one({'name': course_name})
        if course is None:
            course = Course()
            course.name(course_name)
            course.save()
        # If the course is already in the student's list of courses, do nothing
        elif course.name() in [c.name() for c in student.courses.find()]:
            raise RunnerError()

        # If the course is full, raise an error
        if len(course.students.find()) >= MAX_STUDENTS_PER_COURSE:
            raise RunnerError('Course %s is full.' % course_name)

        # Otherwise, bind the course and the student.
        student.courses.attach(course)

    @runner.command('drop', transact=True)
    def drop_course(name, course_name):
        """ (string, string) -> string
        Removes a student from the course, if they are enroled in it. Example
        usage:

            > drop bob CSC148

        An error will be raised if the student doesn't exist.
        """

        # Check to make sure the student exists...
        student = Student.find_one({'name': name})
        if student is None:
            raise RunnerError('Student %s does not exist.' % name)

        # If the course does exist, detach it from the student. We don't have
        # to check if it's attached before detaching it, as no error is raised:
        # the purpose of the detach function is accomplished regardless.
        course = Course.find_one({'name': course_name})
        if course is not None:
            student.courses.detach(course)

    @runner.command('list-courses', transact=True)
    def list_courses(name):
        """ (string) -> string
        List the courses taken by a student. Example usage:

            > list-courses david

        An error will be raised if the student doesn't exist.
        """

        # Check that the student exists
        student = Student.find_one({'name': name})
        if student is None:
            raise RunnerError('Student %s does not exist.' % name)

        # Get a list of names for every course the student takes.
        courses = sorted([c.name() for c in student.courses.find()])
        # If the student isn't taking courses, say so!
        if len(courses) == 0:
            return '%s is not taking any courses.' % name

        return '%s is taking %s' % (name, ', '.join(courses))

    @runner.command('class-list', transact=True)
    def class_list(name):
        """ (string) -> string
        Lists students in a given course. Example usage:

            > class-list CSC148

        Returns a comma-delimited string of courses, or notifies that no one
        is taking that particular course.
        """

        # Try to find the course. If it doesn't exist, no one is taking it.
        course = Course.find_one({'name': name})
        if course is None:
            return 'No one is taking %s.' % name

        # Get students in the course.
        students = [c.name() for c in course.students.find()]
        if len(students) == 0:
            return 'No one is taking %s.' % name

        return ', '.join(sorted(students))

    @runner.command('common-courses', transact=True)
    def common_courses(*students):
        """ ([]string) -> string
        Lists the courses the given set of students has in common.
        Example usage:

            > common-courses george connor

        It raises an error if any of the students don't exist.
        """

        course_sets = []
        error = []
        # For every one of the student given in the CLI...
        for name in students:
            record = Student.find_one({'name': name})
            # If it's not found, message that they don't exist.
            if record is None:
                error.append('ERROR: Student %s does not exist.' % name)
            # Otherwise add their course names to the list of set names.
            else:
                names = [c.name() for c in record.courses.find()]
                course_sets.append(names)

        # If we did get errors, abort and print em.
        if len(error):
            return '\n'.join(error)

        # Start converting the list of course names to sets. Intersect each
        # one down the line, so in the end only names which are in every list
        # will remain.
        common_set = set(course_sets[0])
        for course_set in course_sets[1:]:
            common_set = common_set.intersection(set(course_set))

        return ', '.join(sorted(list(common_set)))
