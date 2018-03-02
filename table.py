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
			currentArg = 0
			for arg in arguments:
				currentType = attributes[currentArg].split()[1] # select type, not name
				
				data = str
				if currentType == "int":
					data = str(int(float(arg))) # float conversion allows truncation if needed
				elif currentType == "float":
					data = str(float(arg))
				elif currentType.split("(")[0] == "varchar" or currentType.split("(")[0] == "char":
					if len(arg) < 2 or arg[0] != "'" or arg[-1] != "'":
						print("!Error: No quotation marks around char/varchar: " + arg)
						return
					else:
						string = arg[1:-1]
						if currentType.split("(")[0] == "varchar":
							length = int(currentType.split(")")[0][8:]) # extract length
						else:
							length = int(currentType.split(")")[0][5:]) # extract length
						data = "'" + string[0:length] + "'" # cut input to max length of varchar

				dataToAdd += data + "|"
				currentArg += 1

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
