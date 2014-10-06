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
#import random
#import string
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
        ''' Maintain student names along with course records
        using dictionary implementation'''
        
        self.studentslog = {}
        self.courselist = {}

    def create(self, name):
        try:
            if name not in self.studentslog:
                self.studentslog[name] = []
            else:
                raise StudentExistsError
            
        except StudentExistsError:
            return ('ERROR: Student {0} already exists.'.format(name))
    
    def delete(self, name):
        try:
            self.studentslog.pop(name)
        except KeyError:
            return ('Cannot delete because {} is not in Database.'.format(name))    
            
    def enrol(self, name, course):       
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
        if course not in self.courselist or len(self.courselist[course]) == 0:
            print ('No one is taking {}.'.format(course))
        else:
            
            #Make a copy of the students in course(immutable copy)
            studentnames = self.courselist[course][:]
            studentnames.sort()
            print (', '.join(studentnames))
                 
#if __name__ == '__main__':
    #a = StudentManagement()
    #a.create('dave')
    #a.create('dab')
    ##a.create('asd')
    #a.enrol('dave', 'z143')
    #a.enrol('dab', 'a12')
    #a.enrol('dab', 'z143')
    ##a.enrol('asd', 'das')
    ##a.drop('dave', '148')
    #print (a.studentslog)
    #print (a.courselist)
    ##a.drop('dave', '148')
    ##print (a.studentslog)
    ##print (a.courselist)
    ##a.listcourses('dave')
    ##a.commoncourses('dfg', 'wer')
    ##a.classlist('z143')
    ##a.delete('dave')
    ##a.delete('dab')
    ##for ch in range(29):
    #chars = string.ascii_uppercase + string.digits
    #ch = [random.choice(chars) for _ in range(100)]
    #print(len(ch))
    #for char in ch:
        #a.create(char)
    #for char in ch:
        #a.enrol(char, '144')
    #a.create('asdd')
    #a.enrol('asdd', '144')    
        
    #print(len(a.courselist['144']))
    #print(len(a.studentslog))
         
    