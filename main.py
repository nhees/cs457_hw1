import sys
import os
from database import Database
from table import Table

currentDb = "NA"

def main():
#	currentDb = "NA"
#    dbs = []

	try:
		sqlInput = input()
		while sqlInput.lower() != ".exit":
			parse_line(sqlInput.split(";")[0])#,currentDb)
			sqlInput = input()
	except EOFError:
		pass # exit
	print("Exiting")

def parse_line(line):#, currentDb):
	global currentDb
	words = line.split(" ")
#put the database instances in a list?
	if line[:2] == "--" or len(line) == 0:
            pass #ignore
	else:
		try:
		#	print("currentDB: "+currentDb+"")
			if words[0].lower() == "create": # found the command create
				if words[1].lower() == "database":
					if not Exists( words[2]):
						Database(words[2])# probably append the database instead
						print("Database '" + words[2] + "' created")
					else:
						print("!Failed to delete database '" + words[2] + "' because it already exists")
				elif words[1].lower() == "table":
					if not TableExist(words[2], currentDb):
						currentTable = Table(words[2], currentDb)
						currentTable.create()

						currentWord = 3
						wordCount = len(words)
						nextWord = words[currentWord]
						#this while loop will run through and
						while currentWord < wordCount:
							atrName = words[currentWord].strip("()")
							if words[currentWord + 1][:3] == "int":
								currentTable.add_column(int,atrName, 0)
							elif words[currentWord + 1][:5] == "float":
								currentTable.add_column(float,atrName, 0)
							elif words[currentWord + 1][:4] == "char":
								currentTable.add_column("char",atrName, words[currentWord + 1][4:].strip("()") )
							elif words[currentWord + 1][:7] == "varchar":
								currentTable.add_column("varchar",atrName, words[currentWord + 1][7:].strip("()") )
							currentWord += 2
						print("Table '" + words[2] + "' created")
					else:
						print("!Failed to create table '"+ words[2] +"' because it already exists")

			elif words[0].lower() == "drop":
				if words[1].lower() == "table":
					if TableExist(words[2], currentDb):
						currentTable = Table(words[2], currentDb)
						currentTable.drop()
						print("Table '" + words[2] + "' deleted")
					else:
						print("!Failed to delete table '" + words[2] + "' because it does not exist")
				elif words[1].lower() == "database":
					if Exists(words[2]):
							DropDb = Database(words[2])
							DropDb.drop()
							print("Database '" + words[2] + "' deleted")
					else:
						print("!Failed to delete database '" + words[2] + "' because it does not exist")

			elif words[0].lower() == "select":
				if TableExist(words[3], currentDb):
					currentTable = Table(words[3], currentDb)
					currentTable.select(words[1])
				else:
					print("!Failed to query table '" + words[3] + "' because it does not exist")

			elif words[0].lower() == "use": # should make sure the db exist
				if Exists(words[1]):
					currentDb = words[1]
					print("Using database '" + words[1] + "'")
				else:
					print("!Failed to use database '" + words[1] + "' because it does not exist")

			elif words[0].lower() == "alter":
				if words[1].lower() == "table":
					if words[3].lower() == "add":
						currentTable = Table(words[2], currentDb)
						if words[5] == "int":
							currentTable.add_column(int,words[4], 0)
						elif words[5]== "float":
							currentTable.add_column(float, words[4], 0)
						elif words[5][:4] == "char":
							currentTable.add_column("char", words[4], words[5][4:].strip("()"))
						elif words[5][:7] == "varchar":
							currentTable.add_column("varchar", words[4], words[5][7:].strip("()"))
						print("Table '" + words[2] + "' modified")
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
