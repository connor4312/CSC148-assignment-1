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
#import student.py
from student import Student,Course, NotEnoughSpaceError, CourseNotFoundError, StudentNotFoundError, CourseAlreadyTakenError
from stack import Stack, EmptyStackError

def undo():
    commands = undo_stack.pop()
    if (commands[0] == "ERROR" or commands[0] == 'list-courses' or commands[0] == 'class-list' or commands[0] == 'common-courses' or commands[0] == 'Unrecognized'):
        pass
    elif (commands[0] == 'enrol'): #REPEATED CODE
        student = find_student(list_of_students, commands[1])
        course = find_course(list_of_courses, commands[2])
        student.drop(course)
        course.drop(student)
    elif (commands[0] == 'drop'): #REPEATED CODE
        student = find_student(list_of_students, commands[1])
        course = find_course(list_of_courses, commands[2])
        student.enrol(course)
        course.enrol(student)         
    elif (commands[0] == 'create'):
        list_of_students.pop()
        #counter = 0
        #for x in list_of_students:
            #if (x.verify(find_student(list_of_students,commands[1]))):
                #list_of_students.pop(counter)
                #break
            #counter += 1

def undo_with_length(number):
    try:
        i = 1
        while (i <= number):
            undo()
            i+= 1
    except (EmptyStackError):
        print("ERROR: No commands to undo")

def student_does_not_exist(name):
    """(str) -> NoneType
    
    name is the name in which we will use to format an error message.
    
    Prints an error message with name as format.
    """
    print("ERROR: Student {} does not exist.".format(name))

def check(list_of_objects, name):
    """(list of Students or list of Courses, str) -> bool
    
    list of objects is a list of students or courses that is passed into the function.
    name is the string that is going to be checked
    
    Loops through the list of students or courses to verify that they have been created before.
    
    """
    for x in list_of_objects:
        if(x.verify(name)):
            return True
        
    return False

def find_course(list_of_courses,name):
    #CHANGE THE DOCSTRING
    """(list of students or list of courses, str) -> student or course
    
    list of objects is a list of students or courses that is passed into the function.
    name is the string that we are looking for
    
    loops through the list of students or courses and returns the one that matches. IF it cannot find a match, an error is raised.
    """
    for x in list_of_courses:
        if(x.verify(name)):
            return x
        
    raise CourseNotFoundError

def find_student(list_of_students,name):
    #CHANGE THE DOCSTRING
    """(list of students or list of courses, str) -> student or course
    
    list of objects is a list of students or courses that is passed into the function.
    name is the string that we are looking for
    
    loops through the list of students or courses and returns the one that matches. IF it cannot find a match, an error is raised.
    """
    for x in list_of_students:
        if(x.verify(name)):
            return x
        
    raise StudentNotFoundError


list_of_courses = []
list_of_students = []   
undo_stack = Stack()

def run():
    """ (NoneType) -> NoneType

    Run the main interactive loop.
    """

    while True:
        command = input('')
        commands = command.split()
        
        if command == 'exit':
            break
        elif commands[0] == 'enrol' and len(commands) == 3:
            #WE HAVE TO VERIFY SPACE
            #WE ALSO HAVE TO CHECK FOR DOUBLE ENROLMENT
            try:
                student = find_student(list_of_students, commands[1])
                course = find_course(list_of_courses, commands[2])
                student.enrol(course)
                course.enrol(student)                
            except (StudentNotFoundError):
                student_does_not_exist(commands[1])
                commands.insert(0, "ERROR")
            except (CourseNotFoundError):
                course = Course(commands[2])
                list_of_courses.append(course)
                student.enrol(course)
                course.enrol(student)
            except (CourseAlreadyTakenError):
                commands.insert(0, "ERROR")
                pass 
            except (NotEnoughSpaceError):
                commands.insert(0, "ERROR")
                print("Course {} is full.".format(commands[2]))
            finally:
                undo_stack.push(commands)
        elif commands[0] == 'create' and len(commands) == 2:
            if (check(list_of_students,commands[1])):
                commands.insert(0,"ERROR")
                print("ERROR: Student {} already exists.".format(commands[1]))
            else:
                student = Student(commands[1])
                list_of_students.append(student)
                undo_stack.push(commands)
        elif commands[0] == 'drop' and len(commands) == 3:
            try:
                student = find_student(list_of_students, commands[1])
                course = find_course(list_of_courses, commands[2])
                student.drop(course)
                course.drop(student)                
            except (StudentNotFoundError):
                commands.insert(0,"ERROR")
                student_does_not_exist(commands[1])
            except (CourseNotFoundError):
                commands.insert(0,"ERROR")
                pass
            finally:
                undo_stack.push(commands)
        elif commands[0] == 'list-courses' and len(commands) == 2:
            try:
                student = find_student(list_of_students, commands[1])
                student.list_courses()
            except (StudentNotFoundError):
                student_does_not_exist(commands[1])
            undo_stack.push(commands)
        elif commands[0] == 'common-courses' and len(commands) == 3:
            try:
                student1 = find_student(list_of_students,commands[1])
            except (StudentNotFoundError):
                student1 = None
                student_does_not_exist(commands[1])
            try: 
                student2 = find_student(list_of_students,commands[2])
            except (StudentNotFoundError):
                student2 = None
                student_does_not_exist(commands[2])
            if not student1 == None and not student2 == None:
                student1.compare(student2)
            undo_stack.push(commands)
        elif commands[0] == 'undo' and len(commands) == 1:
            try:
                undo()
            except(EmptyStackError):
                print("ERROR: No commands to undo")
        elif commands[0] == 'undo' and len (commands)== 2:
            try:
                undo_with_length(int(commands[1]))
            except (ValueError):
                print("{} is not a positive integer".format(commands[1]))
        elif commands[0] == 'class-list' and len(commands) == 2:
            try:
                course = find_course(list_of_courses, commands[1])
                course.list_class()
            except (CourseNotFoundError):
                print("No one is taking {}".format(commands[1]))
            undo_stack.push(commands)
        elif commands[0] == 'checkStudents':
            #FOR DEBUGGING ONLY
            for i in list_of_students:
                print("Person {} has courses {}".format(i.name, str(i.courses)))
        elif commands[0] == 'checkCourses':
            for i in list_of_courses:
                print("Course {} has students {} with an enrollment number of {}".format(i.name, str(i.students),i.enrollment_number))
        elif commands[0] == 'checkUndo':
            for i in range(len(undo_stack)):
                print(undo_stack[i])
        else:
            commands = ["Unrecognized"]
            print("Unrecognized command")
            undo_stack.push(commands)
        for x in list_of_students:
            print(x.to_Str())


if __name__ == '__main__':
    run()