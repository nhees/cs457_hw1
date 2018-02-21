import sys
import os
from database import Database
from table import Table

dbNames =[]
currentDb = "NA"

def main():


	try:
		#runs through the input and processes all of the commands
		sqlInput = input()
		while sqlInput.lower() != ".exit":
			parse_line(sqlInput.split(";")[0])#,currentDb)
			sqlInput = input()
	except EOFError:
		pass # exit
	print("Exiting")
#This is the parser function which processes the input commands.
def parse_line(line):#, currentDb):
	global currentDb
	global dbNames
	words = line.split(" ")
#put the database instances in a list?
	if line[:2] == "--" or len(line) == 0:
            pass #ignore
	else:
		try:
		#	print("currentDB: "+currentDb+"")
			if words[0].lower() == "create": # found the command create
				if words[1].lower() == "database":
					if not Exists( words[2]): # append to the list
						dbNames.append(Database(words[2]))# probably append the database instead
						print("create_database("  + words[2] + ")")
					else:
						print("Database already exists")
				elif words[1].lower() == "table":
					if not TableExist(words[2], currentDb):
						currentTable = Table(words[2], currentDb)
						currentTable.create()
						print("create_table(" + words[2] + ")")


						currentWord = 3
						wordCount = len(words)
						nextWord = words[currentWord]
						#this while loop will run through and
						while currentWord < wordCount:
							if words[currentWord + 1][:3] == "int":
								print("about to call function")
								atrName = words[currentWord].strip("()")
								currentTable.add_column(int,atrName, 0)
								print(" add_column(" + words[2] + ", int" + ", " + words[currentWord].strip("()") + ")")
							elif words[currentWord + 1][:5] == "float":
								currentTable.add_column(float,words[currentWord].strip("()"), 0)
								print(" add_column(" + words[2] + ", float" + ", " + words[currentWord].strip("()") + ")")
							elif words[currentWord + 1][:4] == "char":
								char = "char"
								currentTable.add_column(char,words[currentWord].strip("()"), words[currentWord + 1][4:].strip("()") )
								print(" add_column(" + words[2] + ", char" + ", " + words[currentWord + 1][4:].strip("()") + ", " + words[currentWord].strip("()") + ")")
							elif words[currentWord + 1][:7] == "varchar":
								varchar = "varchar"
								currentTable.add_column(varchar,words[currentWord].strip("()"), words[currentWord + 1][7:].strip("()") )
								print(" add_column(" + words[2] + ", varchar" + ", " + words[currentWord + 1][7:].strip("()") + ", " + words[currentWord].strip("()") + ")")
							currentWord += 2

							print(" --")
					else:
						print("table"+ words[2] +" already exists")

			elif words[0].lower() == "drop":
				if words[1].lower() == "table":
					if TableExist(words[2], currentDb):
						currentTable = Table(words[2], currentDb)
						print("drop_table(" + words[2] + ")")
					else:
						print("ERROR: Table doesn't exist")
				elif words[1].lower() == "database":
					if Exists(words[2]):# delete from list
							found = False
							for db in dbNames: # search through the list to find the right instance
								if (words[2] == db.name):
									db.drop()
									dbNames.remove(db)
									found = True
							if not found: # database exsists but isnt in the list
								DropDb = Database(words[2])
								DropDb.drop()
							print("drop_database(" + words[2] + ")")
					else:
						print("Database doesn't exist")

			elif words[0].lower() == "select":
				print("select(" + words[3] + ", " + words[1] + ")")

			elif words[0].lower() == "use": # should make sure the db exist
				if Exists(words[1]):
					currentDb = words[1]
					print("use_database(" + words[1] + ")")
				else:
					print("database doesn't exist")

			elif words[0].lower() == "alter":
				if words[1].lower() == "table":
					if words[3].lower() == "add":
						if words[5] == "int":
							print("add_column(" + words[2] + ", int" + ", " + words[4] + ")")
						elif words[5]== "float":
							print("add_column(" + words[2] + ", float" + ", " + words[4] + ")")
						elif words[5][:4] == "char":
							print("add_column(" + words[2] + ", char" + ", " + words[5][4:].strip("()") + ", " + words[4] + ")")
						elif words[5][:7] == "varchar":
							print("add_column(" + words[2] + ", varchar" + ", " + words[5][7:].strip("()") + ", " + words[4] + ")")
			else:
				print("Invalid keyword: " + words[0])
		except IndexError:
			print("Invalid line: " + line)

def Exists (name):
    #any(current for current in dbName if current.name == name)
	#should it return if the file exsists?
	#print("in exist")
	filePath = "PA1/"+name+""
#	print("The current filepath: "+filePath+"")
	if os.path.exists(filePath):
			return True

	else:
			return False

    #    for current in dbName:
    #        if current.name == name:
    #            return True

    #    return False
    #return name in dbName
def TableExist(tname, currentDb):
		filePath = "PA1/"+currentDb+"/"+tname+".txt"
		return os.path.isfile(filePath)



if __name__ == "__main__":
	main()
