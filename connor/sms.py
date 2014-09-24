# Assignment 1 - Managing students!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""Interactive console for assignment.

This module contains the code necessary for running the interactive console.
As provided, the console does nothing interesting: it is your job to build
on it to fulfill all the given specifications.

run: Run the main interactive loop.
"""

import sys
from cli.runner import Runner
from somewhatDb.database import db
from somewhatDb.models.student import Student
from somewhatDb.models.course import Course

runner = Runner()
max_students_for_course = 30

@runner.command('exit')
def exit():
    sys.exit()


@runner.command('undo')
def common_courses(actions=1):
    actions = int(actions)
    if db.undo_count() < actions:
        return 'ERROR: No commands to undo.'

    for x in range(actions):
        db.undo()

    return ''

@runner.command('create student', transact=True)
def create_student(name):
    if Student.find_one({'name': name}) is not None:
        return 'ERROR: Student %s already exists.' % name

    student = Student()
    student.set('name', name)
    student.save()

    return ''


@runner.command('enrol', transact=True)
def enrol_student(name, courseName):
    student = Student.find_one({'name': name})
    if student is None:
        return 'ERROR: Student %s does not exist.' % name

    course = Course.find_one({'name': courseName})
    if course is None:
        course = Course()
        course.set('name', courseName)
        course.save()

    if len(course.students.find()) >= max_students_for_course:
        return 'ERROR: Course %s is full.' % courseName

    student.courses.attach(course)

    return ''


@runner.command('drop', transact=True)
def drop_course(name, courseName):
    student = Student.find_one({'name': name})
    if student is None:
        return 'ERROR: Student %s does not exist.' % name

    course = Course.find_one({'name': courseName})
    if course is not None:
        student.courses.detach(course)

    return ''


@runner.command('list-courses')
def list_courses(name):
    student = Student.find_one({'name': name})
    if student is None:
        return 'ERROR: Student %s does not exist.' % name

    courses = sorted([c.get('name') for c in student.courses.find()])
    if len(courses) == 0:
        return '%s is not taking any courses.' % name

    return '%s is taking %s' % (name, ', '.join(courses))


@runner.command('class-list')
def class_list(name):
    course = Course.find_one({'name': name})
    if course is None:
        return 'No one is taking %s.' % name

    students = [c.get('name') for c in course.students.find()]
    if len(students) == 0:
        return 'No one is taking %s.' % name

    return ', '.join(students)


@runner.command('common-courses')
def common_courses(*students):
    course_sets = []
    error = []
    for name in students:
        record = Student.find_one({'name': name})
        if record is None:
            error.append('ERROR: Student %s does not exist.' % name)
        else:
            course_sets.append([c.get('name') for c in record.courses.find()])

    if len(error):
        return '\n'.join(error)

    c = set(course_sets[0])
    for course_set in course_sets[1:]:
        c = c.intersection(set(course_set))

    return ', '.join(sorted(list(c)))

if __name__ == '__main__':
    runner.run()
