# Assignment 1 - Managing Students!
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
"""The back-end data model for the program.

TODO: fill in this doctring with information about your
class(es)!
"""
class NotEnoughSpaceError(Exception):
    pass

class CourseNotFoundError(Exception):
    pass

class CourseAlreadyTakenError(Exception):
    pass

class StudentNotFoundError(Exception):
    pass

class Object:
    def __init__ (self,name):
        self.name = name
    
    def verify(self, Name):
        return self.name == Name

class Student (Object):
    
    def __init__(self, name):
        """ (Student, str) -> NoneType
        
        name is the student's name in which we will use to specify identify the student
        
        Initializes the student with a name, and creates an empty list of courses of which they are currently enrolled in.
        """
        
        self.name = name
        self.courses = []
    
    def enrol(self, course):
        """ (Student, Course) -> NoneType
       
        course is the name of the course that they are to be enrolled in
       
        Adds a course to the student's current list of courses.
       
        """
        
        #Check if the course is greater than 30. Maybe call Course.enrol() first before Student.enrol()???
        if (self.verify_course(course.name) and course.verify_space()):
            self.courses.append(course.name)
    
    def drop(self,course):
        """(Student, str) -> NoneType
        
        course is the name of the course that the student wishes to drop out of
        
        Drops a course from the student's current list of courses
        """
        #if the student isn't taking that course, do nothing
        self.courses.remove(course.name)
        return None
    
    def list_courses (self):
        self.courses.sort()
        output = self.name + " is taking "
        for x in range(len(self.courses)):
            if(x == len(self.courses)-1):
                output += self.courses[x]
            else:
                output += self.courses[x] + ', '
        print(output)
        
    #def verify(self,Name):
        #if self.name == Name:
            #return True
        #return False    
    def compare(self, Student):
        """(Student, Student) -> NoneType
        
        Student is a Student object that we are going to compare.
        
        Finds the same course inbetween each other and prints them out.        
        """
        output = ""
        temp = []
        for x in self.courses:
            for y in Student.courses:
                if x == y:
                    temp.append(x)
        sort (temp)
        for x in range (len(temp)):
            if (x == len(temp)-1):
                output += temp[x]
            else:
                output += temp[x] + ", "
        print(output)
    
    def verify_course(self,Course):
        """(Student, str) -> bool
        
        Course is the course name that the student is verifying if they are already enrolled
        
        Raises an exception if the person is currently taking the course, and returns false if they aren't
        """
        for x in self.courses:
            if x == Course:
                raise CourseAlreadyTakenError
        return True
    
    def to_Str(self):
        return self.name
    
class Course (Object):
    
    def __init__ (self, name):
        """ (Course, str) -> NoneType
        
        name is the name of the course that will be instantiated
        
        Creates a course under the name "name"
        """
        self.name = name
        self.enrollment_number = 0
        self.students = []
        
    def list_class (self):
        """(Course) -> NoneType
        
        Lists all the people taking the current course in alphabetical order.
        """
        self.students.sort()
        output = ""
        for x in range(len(self.students)):
            if (x == len(self.students)-1):
                output += self.students[x]
            else:
                output += self.students[x] + ", "
        print (output)
    
    def enrol(self, Student):
        """(Course, Student) -> NoneType
        
        Student is the Student object that will be enrolling in this course.
        
        Adds a Student to the course's list of people enrolled
        """
        if (self.verify_space()):
            self.students.append(Student.name)
            self.enrollment_number+=1
            return None
        else:
            raise NotEnoughSpaceError
    
    def drop(self,Student):
        """(Course, Student) -> NoneType
        
        Student is the Student object that will be dropping out of this course.
        
        Drops a student from the course's list of people enrolled.
        """
        #if person doesn't exist, ignore it
        #if NO STUDENT NAMED NAME EXISTS, ERROR MESSAGE
        self.students.remove(Student.name)
        self.enrollment_number -= 1
        
        return None
    
    def verify_space(self):
        """(Course) -> bool
        
        Verifies if the object has les than 30 people in it.
        """
        return self.enrollment_number<30
            
        