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

	def update(self, setAttr, newValue, whereAttr, oldValue):
		#print("in the update function")
		#quotes = ''
		#edit the where attr is equal to old value
		#to where set attr is equal to new vlaue
		tbFile = open(self.filePath, "r+")
		testmetaData = tbFile.readline()
		metaData = testmetaData.split("|")
		#the attribute that will be changed
		for i in metaData:
			if setAttr in i:
				setAttrIndex = metaData.index(i)
		#the attribute that we are looking for

		for i in metaData:
			 if whereAttr in i:
				 whereAttrIndex = metaData.index(i)

		lines = tbFile.readlines()
		tbFile.seek(0)
		tbFile.truncate()

		tbFile.write(testmetaData) #rewriting the metadata line

		for line in lines:
				testline = line.split("|")
				if oldValue == testline[whereAttrIndex].strip("''"):
					line = line.replace(testline[setAttrIndex].strip("''"), newValue)
				tbFile.write(line)

	def delete(self, attribute,relation, value):
	#	print("In delete function")
		tbFile = open(self.filePath, "r+")
		testmetaData = tbFile.readline()
		metaData = testmetaData.split("|")
		#the attribute that will be changed
		for i in metaData:
			if attribute in i:
				attrIndex = metaData.index(i)
		lines = tbFile.readlines()
		tbFile.seek(0)
		tbFile.truncate()

		tbFile.write(testmetaData) # rewriting themetaData line

		for line in lines:
				testline = line.split("|")

				if relation == '=':
					if testline[attrIndex].strip("''") != value:
						tbFile.write(line)

				elif relation == '<':

					if float(testline[attrIndex]) > float(value):
						tbFile.write(line)
				else:
					#print("Old value "+testline[attrIndex]+ " value: " + value +"")

					if float(testline[attrIndex]) < float(value):
						print("Old value "+testline[attrIndex]+ " value: " + value +"")
						tbFile.write(line)

	#deletes the table file
	def drop(self):
		os.remove(self.filePath)

# Insert: adds a new tuple to the table
# param arguments:
#       tuple to be added to the table (e.g. [1,'Product',4.99]
# algorithm:
#     Ensures that the tuple is of the right length. Then, applies
#     basic type enforcement (var/chars must have quotation marks
#     and be of the correct length, ints should not have decimal
#     values). Finally, adds the tuple to the bottom of the table
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
			for i, arg in enumerate(arguments):
				currentType = attributes[i].split()[1] # select type, not name

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
