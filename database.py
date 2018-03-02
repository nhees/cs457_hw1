import os
from table import Table

DIRECTORY = "PA2/"

DIRECTORY = "PA2/"

class Database:
# Creates and Destroys databases
# Initialized with a database name

	#Functions
	#Constructor
	def __init__(self, dbName ):
	#Variables
		self.name = dbName
		self.tableNames = [] # our array
		self.create()

#Create: This functions creates the folder that is representative of the
#Database
	#it will only create the folder if the
	def create(self):
		filePath = DIRECTORY+ self.name+""
		#checks if the directory already exists
		if not os.path.exists(filePath):
			os.makedirs(filePath)

#Drop: this function is in charge of deleting the folder that represents the databse
	def drop(self):
		filepath = DIRECTORY+self.name+""
		os.system("rm -rf " + filepath)
<<<<<<< HEAD
=======

	def select(self, attributes, tables, conditions):
		joinedTable = []

		# from statement
		for tableName in tables:
			currentTable = Table(tableName, self.name)
			tbFile = open(currentTable.filePath, "r")
			
			for line in tbFile:
				joinedTable.append(line.split("|")[:-1]) # -1 because the last item is \n
				# multitable implementation to be worried about later
		
		# where statement
		
		
		# select statement
		currentAttr = 0
		for attribute in joinedTable[0]: # row 0 is the metadata
			attrName = attribute.split()[0]
			if "*" not in attributes and attrName not in attributes:
				for row in joinedTable:
					row.pop(currentAttr) # remove the whole column

			currentAttr += 1
		
		# print result
		for row in joinedTable:
			print(row)
					
					
>>>>>>> a1c47bbe16d5775be7403a1135c60ee2f4979cad
