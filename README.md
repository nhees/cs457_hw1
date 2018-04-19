# cs457_hw1
PA3 was completed by Nina Hees and Bryson Lingenfelter
Documentation for PA3:

pa3.py:
This file processes the input commands and parses the information. It collects the command first, then determines whether the object is a table or database. From there the command is processed and the appropriate class is called upon. The only command not handled by database.py or table.py is the USE command which is solved by setting the global variable currentDb to the database that is being called upon.

database.py:
This file holds the database class, which handles database operations.
- Create: creates the database by adding a new folder in the PA3 folder
- Drop: removes the table by deleting its folder
- Select: allows the user to view a table, with certain attributes and tuples filtered out. First loads the table into memory, then removes tuples that don't match all of the supplied conditions, then removes attributes which aren't being selected, and finally prints the remaining table cells.
- Join: deals with all join functionality which consists of inner and outer left join between specified tables. Both joins are implemented using a nested loop. In the case of the inner join, each tuple in table one is concatenated with each tuple in table two for which the condition succeeds. The results are appended to the joined table. In the case of outer join, the tuple from table one is still appended to the joined table even if it did not match any tuples in table two. A flag called "successfulMatch" is used to monitor whether the tuple needs to be appended if it is an outer join.

table.py
This file holds the table class. The tables are represented by a file within the appropriate database folder. The first line of the file will holds the attribute types and names. The attributes are added via the add_column function within the class. The create table adds the file. The drop table deletes the file.
Supported functions:
- Create: creates the table by adding a new folder and text file in the PA3 folder
- Drop: removes the table by deleting its folder
- Alter: lets the user add a new attribute to the table.
- Insert: adds a new tuple to the table. Applies type enforcement, then appends the tuple to the end of the table file
- Delete: deletes a tuple from the table.
- Update: updates the value of a tuple in the table

To run: python3 pa3.py < (fileName) OR
        python3 pa3.py

Databases are stored in a local folder titled PA3
