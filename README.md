# cs457_hw1
This is for our database class
PA1 was completed by Nina Hees and Bryson Lingenfelter
Documentation for PA1:

main.py:
This file processes the input commands and parses the information. It collects the command first which can be create, drop, use, select or alter. Then determines which object table or database. From there the command is processed and the appropiate class is called upon.A list of database names is stored globally so the correct instance can be refered to when needed. The ony command that doesnt have a function for it is the USE command which is solved by setting the global variable currentDb to the current database that is being called upon.

database.py:
This file holds the database class where when call upon a database can be created or deleted. When creating a database it creates a folder to represent the database within the PA1 folder. When dropping the database it deletes said folder. 

table.py 
This file holds the table class. The tables are represented by a file within the appropiate database folder. The first line of the file will holds the attribute types and names. The attributes are added via the add_column function within the class. The create table adds the file. The drop table deletes the file. The select function allows the user to view requested parts of the table and alter lets the user change the attribute types within the table. 
 
 
 
 PLEASE NOTE ALL OUTPUT IS SUPPOSE TO BE LOCATED IN A FOLDER NAMED PA1
