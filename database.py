import os
from table import Table

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

# Select: this function queries the database
# param attributes:
#       list of attribute names to select (e.g. [pid,price])
# param tables:
#       list of tables to be selected (currently only 1 is supported)
# param conditions:
#       list of conditions to apply (e.g. [price = 1,pid < 5]
# algorithm:
#     selects the first table in the list and loads it. For each condition in 
#     the condition list, removes tuples that don't match the condition. Then,
#     removes all columns with attributes not in the attribute list. Finally,
#     prints the remaining elements in the table
	def select(self, attributes, tables, conditions):
		joinedTable = []
		
		if len(attributes[0]) == 0:
			print("!Error: nothing to select")
			return

		# from statement
		currentTable = Table(tables[0].lower(), self.name) # only worry about the first table (for now!)
		tbFile = open(currentTable.filePath, "r")
			
		for line in tbFile:
			joinedTable.append(line.split("|")[:-1])
	
		# where statement
		for condition in conditions:
			words = condition.split()
			if len(words) != 3:
				print("!Failed to select: invalid condition '" + condition + "'")
				return
			
			condAttribute = words[0]
			condOperator = words[1]
			condParameter = words[2]

			attrIndex = 0
			for attribute in joinedTable[0]: # find condition attribute
				attrName = attribute.split()[0]
				if attrName == condAttribute:
					break # attr index has been found
				attrIndex += 1
			if attrIndex == len(joinedTable[0]): # attr wasn't found
				print("!Failed to select: couldn't apply constraint to attribute '" + condAttribute + "'")
				return

			if condOperator == "!=":
				for row in joinedTable[1:]: # 1: because attribute row is skipped
					if row[attrIndex] == condParameter:
						joinedTable.remove(row) # remove row
			elif condOperator == "=":
				for row in joinedTable[1:]:
					if row[attrIndex] != condParameter:
						joinedTable.remove(row)
			elif condOperator == "<":
				for row in joinedTable[1:]:
					if float(row[attrIndex]) >= float(condParameter):
						joinedTable.remove(row)
			elif condOperator == ">":
				for row in joinedTable[1:]:
					if float(row[attrIndex]) <= float(condParameter):
						joinedTable.remove(row)
			else:
				print("!Failed to select: unknown operator '" + condOperator + "'")
				return

		# select statement
		for i, attribute in enumerate(joinedTable[0]): # row 0 is the metadata
			attrName = attribute.split()[0]
			if "*" not in attributes and attrName not in attributes:
				for row in joinedTable:
					row.pop(i) # remove the whole column
		
		# print result
		for row in joinedTable:
			rowText = "| "
			for item in row:
				rowText += item + " | "
			print(rowText)
