



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
import student
from stack import Stack, EmptyStackError

def run():
    """ (NoneType) -> NoneType

    Run the main interactive loop.
    """
    database = student.StudentManagement()
    storecommands = Stack()
    commandcheck = Stack()

    while True:
        command = input('').split()
        #command = command.split()
        storecommands.push(command)
        if command == []:
            commandcheck.push('ERROR: Invalid input')
            print('Unrecognized command!')        
        elif command[0] == 'exit':
            break
        elif len(command) <= 2 and command[0] == 'undo':
            storecommands.pop()
            ntimes = 0
            #print (command[0:2])

            if len(command) == 2:
                try:
                    if int(command[1]) > 0:
                        ntimes = int(command[1])
                    else:
                        print ('ERROR: {} is not a positive natural number.'.format(command[1]))
                        
                except ValueError:
                    print ('ERROR: {} is not a positive natural number.'.format(command[1]))
            else:  # Assumed single undo line
                ntimes = 1
            
            while ntimes != 0:
                try:
                    ntimes = ntimes - 1
                    #print (command[0:2])
                    commandpop = storecommands.pop()
                    resultcheck = commandcheck.pop()

                    
                    if commandpop[0:2] == ['create', 'student'] and str(resultcheck).split()[0] not in ['ERROR:']:
                        #print (command[0:2])
                        database.delete(commandpop[2])
                    elif commandpop[0] == 'enrol' and str(resultcheck).split()[0] not in ['ERROR:', 'Nothing']:
                        database.drop(commandpop[1], commandpop[2])
                    elif commandpop[0] == 'drop' and str(resultcheck).split()[0] not in ['ERROR:', 'Nothing']:
                        database.enrol(commandpop[1], commandpop[2])
                   
                    
                except EmptyStackError:
                    ntimes = 0 
                    print ('ERROR: No commands to undo.')
                    
                        
        elif len(command) == 3 and command[0:2] == ['create', 'student']:

            commandcheck.push(database.create(command[2]))
            temp = []
            temp.append(commandcheck.pop())
            if temp[-1] != None:
                print (temp[-1])
            commandcheck.push(temp.pop())
            
        elif len(command) == 3 and command[0] == 'enrol':
            commandcheck.push(database.enrol(command[1], command[2]))
            temp = []
            temp.append(commandcheck.pop())
            if temp[-1] not in [None, 'Nothing']:  
                print (temp[-1])
            commandcheck.push(temp.pop())
            
        elif len(command) == 3 and command[0] == 'drop':
            commandcheck.push(database.drop(command[1], command[2]))
            temp = []
            temp.append(commandcheck.pop())
            if temp[-1] not in [None, 'Nothing']:
                print (temp[-1])
            commandcheck.push(temp.pop())
            
        elif len(command) == 2 and command[0] == 'list-courses':
            commandcheck.push(database.listcourses(command[1]))
        elif len(command) == 3 and command[0] == 'common-courses':
            commandcheck.push(database.commoncourses(command[1], command[2]))
        elif len(command) == 2 and command[0] == 'class-list':
            commandcheck.push(database.classlist(command[1]))
        else:
            commandcheck.push('ERROR: Invalid input')
            print('Unrecognized command!')

if __name__ == '__main__':
    run()

