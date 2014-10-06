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
import stack

def run():
    """ (NoneType) -> NoneType

    Run the main interactive loop.
    """
    database = student.StudentManagement()
    storecommands = stack.Stack()
    commandcheck = stack.Stack()

    while True:
        command = input('').split()
        #command = command.split()
        if command[0] != 'undo':
            storecommands.push(command)  #Ignore Undo commands
       
        if command == 'exit':
            break
        elif command == []:
            commandcheck.push('Error:')
            print('Unrecognized command!')
        elif len(command) <= 2 and command[0] == 'undo':            
            ntimes = 0
            
            #Collect number of commands stored
            templist = []
            while not storecommands.is_empty():
                templist.append(storecommands.pop())
            templist2 = templist[:]  #Make copy of list storing commands
            while len(templist) != 0:
                storecommands.push(templist.pop())
            #----------------------------------
            
            if len(templist2) == 0:
                print ('ERROR: No commands to undo.')
            else:
                if len(command) == 1:  #Only for single undo word
                    ntimes = 1
                else:
                    if int(command[1]) <= 0:  #not isinstance(command[1], int) or 
                        print ('ERROR: {} is not a positive natural number.'.format(command[1]))
                    else:
                        ntimes = int(command[1])
                while ntimes != 0:
                    commandpop = storecommands.pop()
                    resultcheck = commandcheck.pop()         
                    if commandpop[0] == 'create' and resultcheck not in ['Error:']:
                        database.delete(commandpop[2])
                    elif commandpop[0] == 'enrol' and resultcheck not in ['Error:', 'Nothing']:
                        
                        database.drop(commandpop[1], commandpop[2])
                    elif commandpop[0] == 'drop' and resultcheck not in ['Error:', 'Nothing']:
                        database.enrol(commandpop[1], commandpop[2])
                    ntimes = ntimes - 1
        elif len(command) == 3 and command[0] == 'create':

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
            commandcheck.push('Error:')
            print('Unrecognized command!')

if __name__ == '__main__':
    run()
