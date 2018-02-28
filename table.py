import os

DIRECTORY = "PA2/"

class Table:
# Handles table operations
# Initialized with a table name, can perform various operations on the table

	#constructor
	#declares the variables: tnme, db and filePath
	def __init__(self, tableName, db ):
		self.tname = tableName
		self.db = db #name of the database the table is located in
		self.filePath = DIRECTORY+self.db+"/"+self.tname+".txt"


	#Creates the file that will represent the table
	def create(self):
		#filePath= "PA1/"+self.db+"/"+self.tname+".txt"
		open(self.filePath,"a")
		#print("create the table")


	#deletes the table file
	def drop(self):
		os.remove(self.filePath)

	#delete file and metadata from the metadata file

	# displays the table information
	def select(self, selected):
		tbFile = open(self.filePath, "r")
		metadata = tbFile.readline()
		attributes = metadata.split("|")

		selectedMetaData = ""

		for attribute in attributes:
			if len(attribute) > 0 and ((attribute.split(" "))[0] == selected or selected == "*"): # allows for selecting all or a single column
				selectedMetaData += (attribute + " | ")

		print(selectedMetaData)

	#inserts tuple into table
	def insert(self, arguments):
		tbFile = open(self.filePath, "r")
		metadata = tbFile.readline()
		attributes = metadata.split("|")

		dataToAdd = "\n"

		successfulInsert = True

		if len(arguments) != len(attributes) - 1:
			print("Invalid tuple length: " + str(len(arguments)) + " (there are " + str(len(attributes) - 1) + " attributes)")
			successfulInsert = False
		else:
			for arg in arguments:
				# type check
				dataToAdd += arg + "|"

		wrFile = open(self.filePath, "a")
		wrFile.write(dataToAdd)
		return successfulInsert

	#adds and attribute to the table
	def add_column(self,type, name, length):

		file = open(self.filePath,"a")

		if(type == int):
			file.write(name +" int" + "|")
		elif(type == float):
			file.write(name+" float" + "|")
		elif(type == "char"):
			file.write(name+ " char("+ length +")" + "|")
		else:
			file.write(name + " varchar("+length+")" + "|")
