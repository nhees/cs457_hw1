# cs457_hw1
PA2 was completed by Nina Hees and Bryson Lingenfelter
Documentation for PA2:

pa2.py:
This file processes the input commands and parses the information. It collects the command first, then determines whether the object is a table or database. From there the command is processed and the appropriate class is called upon. The only command not handled by database.py or table.y is the USE command which is solved by setting the global variable currentDb to the database that is being called upon.

database.py:
This file holds the database class, which handles database operations.
- Create: creates the database by adding a new folder in the PA2 folder
- Drop: removes the table by deleting its folder
- Select: allows the user to view a table, with certain attributes and tuples filtered out. First loads the table into memory, then removes tuples that don't match all of the supplied conditions, then removes attributes which aren't being selected, and finally prints the remaining table cells.

table.py
This file holds the table class. The tables are represented by a file within the appropriate database folder. The first line of the file will holds the attribute types and names. The attributes are added via the add_column function within the class. The create table adds the file. The drop table deletes the file.
Supported functions:
- Create: creates the table by adding a new folder and text file in the PA2 folder
- Drop: removes the table by deleting its folder
- Alter: lets the user add a new attribute to the table.
- Insert: adds a new tuple to the table. Applies type enforcement, then appends the tuple to the end of the table file
- Delete: deletes a tuple from the table.
- Update: updates the value of a tuple in the table

To run: python3 pa2.py < (fileName) OR
        python3 pa2.py

Databases are stored in a local folder titled PA2
