

# Assignment 1 - Managing Students!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
# Anish Krishna, c3krishn
#
#
# ---------------------------------------------
"""The back-end data model for the program.

TODO: fill in this doctring with information about your
class(es)!
"""
class StudentExistsError(Exception):
    pass
class StudentNotExistsError(Exception):
    pass
class CourseFullError(Exception):
    pass
class StudentBothNotExistsError(Exception):
    pass

class StudentManagement(object):
    
    def __init__(self: 'StudentManagement') -> None:
        '''(Student, str) -> NoneType
        
        Initializes empty dictionaries studentslog and courselist to store
        student names and course informations using dictionary implementation
        
        Store all names of student(s) along with the course(s) they are taking
        in dictionary studentslog. Store all course(s) and the student(s)
        enrolled in those course(s) in the dictionary courselist'''
        
        self.studentslog = {}
        self.courselist = {}

    def create(self, name):
        '''(StudentManagement, str) -> NoneType
        Create student named with name argument'''
        try:
            if name not in self.studentslog:
                self.studentslog[name] = []
            else:
                raise StudentExistsError
            
        except StudentExistsError:
            return ('ERROR: Student {0} already exists.'.format(name))
    
    def delete(self, name):
        '''(StudentManagement, str) -> NoneType
        Delete student named with <name> argument'''        
        
        try:
            self.studentslog.pop(name)
        except KeyError:
            return ('Cannot delete because {} is not in Database.'.format(name))    
            
    def enrol(self, name, course):
        '''(StudentManagement, str, str) -> NoneType
        Enrol student named with <name> argument in course in <course>
        argument'''        
        try:
            if name not in self.studentslog:
                raise StudentNotExistsError
            elif course in self.courselist and \
                 (len(self.courselist[course]) >= 30):
                raise CourseFullError
            else:
                if course not in self.courselist:
                    self.courselist[course] = []                
                
                if name not in self.courselist[course]:  #Do nothing if student already in course
                    
                    self.studentslog[name].append(course)
                    self.courselist[course].append(name)
                else:  #Return a note that nothing was done
                    return ('Nothing')
        except StudentNotExistsError:
            return ('ERROR: Student {0} does not exist.'.format(name))
        except CourseFullError:
            return ('ERROR: Course {0} is full.'.format(course))         
         
    def drop(self, name, course):
        '''(StudentManagement, str, str) -> NoneType
        Drop student named with <name> argument from course in <course>
        argument'''         
        try:
            if name not in self.studentslog:
                raise StudentNotExistsError
            else:
                if course in self.studentslog[name]:  #Do nothing to student not in course 
                    self.studentslog[name].remove(course)
                    self.courselist[course].remove(name)
                else: #Return a note that nothing was done
                    return ('Nothing')
        except StudentNotExistsError:
            return ('ERROR: Student {0} does not exist.'.format(name))
    
    def listcourses(self, name):
        '''(StudentManagement, str) -> str
        Return a list of courses taken by student named in <name>'''
        try:
            if name not in self.studentslog:
                raise StudentNotExistsError
            elif len(self.studentslog[name]) == 0:
                print('{0} is not taking any courses.'.format(name))
            else:
                listcourse = []
                for courses in self.studentslog[name]:
                    listcourse.append(courses)
                listcourse.sort()
                courses = ', '.join(listcourse)                
                print ('{0} is taking {1}'.format(name, courses))
        except StudentNotExistsError:
            print('ERROR: Student {0} does not exist.'.format(name))        
        
    def commoncourses(self, name1, name2):
        '''(StudentManagement, str, str) -> str
        Return a list of common courses between student named in <name1>
        argument and student named in <name2> argument'''         
        try:
            if name1 not in self.studentslog and name2 not in self.studentslog:
                raise StudentBothNotExistsError
            elif name1 not in self.studentslog or name2 not in self.studentslog:
                traitor = ''
                if name1 not in self.studentslog:
                    traitor += name1
                else:
                    traitor += name2
                raise StudentNotExistsError
            else:
                commoncourses = []
                for course in self.studentslog[name1]:
                    if course in self.studentslog[name2]:
                        commoncourses.append(course)
                commoncourses.sort()
                print (', '.join(commoncourses))
        except StudentBothNotExistsError:
            print('ERROR: Student {0} does not exist.'.format(name1))
            print('ERROR: Student {0} does not exist.'.format(name2))
        except StudentNotExistsError:
            print('ERROR: Student {0} does not exist.'.format(traitor))
            
    def classlist(self, course):
        '''(StudentManagement, str) -> str
        Return the list of students taking the course named in <course> argument
        by their provided student names'''         
        
        if course not in self.courselist or len(self.courselist[course]) == 0:
            print ('No one is taking {}.'.format(course))
        else:
            
            #Make a copy of the students in course(immutable copy)
            studentnames = self.courselist[course][:]
            studentnames.sort()
            print (', '.join(studentnames))
                 

         
    

