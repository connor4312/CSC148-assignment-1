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
"""
Yes, this file is empty! This program is fairly modular, and the logic is
distributed across several files. MarkUs doesn't allow us to submit
directories, so think of each underscore in
filenames as being a seperate folder.

The cli_runner is reponsible for dispatching console commands. Commands (found
in cli_commands_*.py) are bound to it. When it receives input, it parses the
arguments and dispatches the command to the appropriate function.

Most of the actual logic is done in the Mongo-inspired "somewhatDb". It's
basically a simple NoSQLish database implementation, using Python dicts. The
datastore engine can be found in somewhatDb_database, then we built an ORM
layer onto it: somewhatDb_model.py. Models can have relations -- in this case
we only have a many-to-many relation for courses and students.

In this database layer is also a "transaction" store, which enables sets of
database transactions to be rolled back at the database level.

So, why this architecture? In part, SOLID. While implementing more intricate
features such as an inversion layer are outside the scope of the assignment,
we still tried to follow good OO design principles. The CLI commands shouldn't
know or care how data is being stored, the models shouldn't be involved
in how datastore operations get rolled back, the command resolver should not
worry about how stdin input will be given, and so on.


Test coverage report: (generated with https://pypi.python.org/pypi/coverage)

Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
cli_commands_enrolment                  64      0   100%
cli_commands_meta                       21      0   100%
cli_errors                               2      0   100%
cli_runner                              28      0   100%
sms                                     10      2    80%   34-35
somewhatDb_associations_manyToMany      28      0   100%
somewhatDb_database                     86      0   100%
somewhatDb_model                        27      0   100%
somewhatDb_models_course                 7      0   100%
somewhatDb_models_student                7      0   100%
somewhatDb_transactor                   17      0   100%
student_test                             6      0   100%
test_database                            3      0   100%
test_models                              4      0   100%
test_sms                                 4      0   100%
------------------------------------------------------------------
TOTAL                                  314      2    99%
"""
