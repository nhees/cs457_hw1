import sys
import os
from database import Database
from table import Table

currentDb = "NA"
DIRECTORY = "PA4/"
inTransaction = False
locks = []
memBuffer = []

def main():
    if not os.path.exists(DIRECTORY + "Locks"):
        os.makedirs(DIRECTORY + "Locks")
    try:
        #runs through the input and processes all of the commands
        sqlInput = input().rstrip("\r\n")
        while sqlInput.lower() != ".exit":
            while sqlInput[:2] != "--" and len(sqlInput) != 0 and not ";" in sqlInput:
                #allow multi-line input. A space is added to the end of the line
                #(double spaces are filtered out anyway)
                sqlInput = sqlInput + " " + input("-->").strip("\r\n")
            parse_line(sqlInput.split(";")[0])#,currentDb)
            sqlInput = input().rstrip("\r\n")
    except EOFError:
        #no more commands, so exit
        pass
    print("Exiting")

#This is the parser function which processes the input commands.
def parse_line(line):
    global currentDb
    global inTransaction
    global locks
    global memBuffer

    words = line.split()

    if line[:2] == "--" or len(line) == 0:
            pass #ignore
    else:
        if words[0].lower() == "create":
            if words[1].lower() == "database":
                if not db_exists(words[2].lower()):
                    currentDatabase = Database(words[2].lower())
                    currentDb = words[2].lower()
                    currentDatabase.create()
                    print("Database '" + words[2] + "' created")
                else:
                    print("!Failed to create database '" + words[2]
                          + "' because it already exists")
            elif words[1].lower() == "table":
                if currentDb == "NA":
                    print("!Failed to create table '"+ words[2]
                          + "' because no database is being used")
                else:
                    argStart = words[2].find('(')
                    tableName = words[2]
                    if argStart != -1: #no space between table name and parenthesis
                        tableName = words[2][:argStart]
                        words.insert(3, words[2][argStart + 1:])

                    if not tb_exists(tableName.lower(), currentDb):
                        currentTable = Table(tableName.lower(), currentDb)
                        currentTable.create()

                        currentWord = 3
                        wordCount = len(words)
                        nextWord = words[currentWord]

                        while currentWord < wordCount:
                            #calls the add_column method on each argument
                            atrName = words[currentWord].strip("()")
                            atrType = words[currentWord + 1]
                            if atrType[:3] == "int":
                                currentTable.add_column(int,atrName, 0)
                            elif atrType[:5] == "float":
                                currentTable.add_column(float,atrName, 0)
                            elif atrType[:4] == "char":
                                currentTable.add_column("char",atrName,
                                             atrType[atrType.find('(')+1:atrType.find(')')])
                            elif atrType[:7] == "varchar":
                                currentTable.add_column("varchar",atrName,
                                             atrType[atrType.find('(')+1:atrType.find(')')])
                            currentWord += 2
                        print("Table '" + tableName + "' created")
                    else:
                        print("!Failed to create table '" + tableName
                              + "' because it already exists")
            else:
                print('Syntax: "create <table | database> '
                      + '[(<tableAttrName> <tableAttrType>, ... )]"')

        elif words[0].lower() == "drop":
            if words[1].lower() == "table":
                if currentDb == "NA":
                    print("!Failed to delete table '" + words[2]
                          + "' because no database is being used")
                elif tb_exists(words[2].lower(), currentDb):
                    currentTable = Table(words[2].lower(), currentDb)
                    currentTable.drop()
                    print("Table '" + words[2] + "' deleted")
                else:
                    print("!Failed to delete table '" + words[2]
                          + "' because it does not exist")
            elif words[1].lower() == "database":
                #delete from list
                if db_exists(words[2].lower()):
                        if currentDb == words[2].lower():
                            #dropping the current database
                            currentDb = "NA"
                        currentDb = Database(words[2].lower())
                        currentDb.drop()
                        print("Database '" + words[2] + "' deleted")
                else:
                    print("!Failed to delete database '" + words[2]
                          + "' because it does not exist")

        elif words[0].lower() == "select":
            if currentDb == "NA":
                print("!Failed to query table '" + words[3]
                      + "' because no database is being used")
            else:
                attributes = [] #what columns to select
                tables = []     #what tables to join
                conditions = [] #what conditions to apply
                tableBuff = ""
                currentWord = 1
                tablStart = 0
                condStart = 0

                for word in words[1:]:
                    if word.lower() == "from":
                        attributes = "".join(words[1:currentWord]).split(",")
                        tablStart = currentWord + 1
                    elif word.lower() == "where" or word.lower() == "on":
                        tableBuff = " ".join(words[tablStart:currentWord])
                        condStart = currentWord + 1
                    currentWord += 1

                if condStart != 0:
                    #the where keyword was used
                    conditions = " ".join(words[condStart:currentWord]).split(",")
                else:
                    tableBuff = " ".join(words[tablStart:currentWord])

                # table parsing
                if tableBuff.find(",") != -1:
                    tables = tableBuff.split(",")
                    tables.insert(0,"inner")
                elif tableBuff.find("inner join") != -1:
                    tables = tableBuff.split("inner join")
                    tables.insert(0,"inner")
                elif tableBuff.find("left outer join") != -1:
                    tables = tableBuff.split("left outer join")
                    tables.insert(0,"l-outer")
                elif tableBuff.find("right outer join") != -1:
                    tables = tableBuff.split("right outer join")
                    tables.insert(0,"r-outer")
                else:
                    tables.append("inner")
                    tables.append(tableBuff)

                #make sure table names are valid before calling function
                for line in tables[1:]:
                    tableName = line.split()[0]
                    if not tb_exists(tableName.lower(), currentDb):
                        print("!Failed to select from '" + tableName
                              + "' because it does not exist")
                        return

                selectDB = Database(currentDb)
                selectDB.select(attributes, tables, conditions, inTransaction, memBuffer)

        elif words[0].lower() == "use":
            if db_exists(words[1].lower()):
                currentDb = words[1].lower()
                print("Using database '" + words[1] + "'")
            else:
                print("!Failed to use database '" + words[1] + "' because it does not exist")

        elif words[0].lower() == "alter":
            if words[1].lower() == "table":
                if currentDb == "NA":
                    print("!Failed to alter table '" + words[2]
                          + "' because no database is being used")
                elif words[3].lower() == "add":
                    if tb_exists(words[2].lower(), currentDb):
                        currentTable = Table(words[2].lower(), currentDb)
                        if words[5] == "int":
                            currentTable.add_column(int,words[4], 0)
                        elif words[5]== "float":
                            currentTable.add_column(float, words[4], 0)
                        elif words[5][:4] == "char":
                            currentTable.add_column("char", words[4],
                                                    words[5][4:].strip("()"))
                        elif words[5][:7] == "varchar":
                            currentTable.add_column("varchar", words[4],
                                                    words[5][7:].strip("()"))
                        print("Table '" + words[2] + "' modified")
                    else:
                        print("!Failed to alter table '" + words[2]
                              + "' because it does not exist")
            else:
                print('Syntax: "alter table add <attrName> <attrType>"')

        elif words[0].lower() == "update":
            FILE = words[1].lower()
            print("Updating " + words[1]+ ":")
            currentTable = Table(FILE, currentDb)
            if words[2] == "set":
                if inTransaction:
                    # Acquire lock
                    if currentTable.tname not in locks:
                        print("  Acquiring lock")
                        if not acquire_lock(currentTable.tname):
                            # don't do anything: table is locked
                            print("!Error: " + currentTable.tname + " is locked")
                            return

                if not inTransaction and os.path.exists(DIRECTORY + "Locks/"
                                                        + currentTable.tname + ".lock"):
                    print("!Error: " + currentTable.tname + " is locked")
                    return

                attr = words[3]
                newValue = words[5].strip("''")
                print ("  Setting attribute : " + attr + " to new value: " + newValue + " ")
                if words[6] == "where":
                    whereAttr = words[7]
                    oldValue = words[9].strip("''")
                    memBuffer.append(FILE)
                    currentTable.update(attr,newValue, whereAttr, oldValue,
                                        inTransaction, memBuffer)
                    print("  Where " + whereAttr + " is: " + oldValue + " ")
                else:
                    print("Invalid no where command")
            else:
                print("Invalid command")

        elif words[0].lower() == "insert":
            if currentDb == "NA":
                    print("!Failed to insert to table '" + words[2]
                          + "' because no database is being used")
            elif words[1].lower() == "into":
                if tb_exists(words[2].lower(), currentDb):
                    arguments = "".join(words[3:]).replace('(',',').replace(')','').split(',')
                    if arguments[0].lower() == "values":
                        currentTable = Table(words[2].lower(), currentDb)
                        if currentTable.insert(arguments[1:]):
                            print("1 new record inserted")
                    else:
                        print("Invalid insertion command: " + arguments[0])
                else:
                    print("!Failed to insert into table '" + words[2]
                          + "' because it does not exist")

        elif words[0].lower() == "delete":
            FILE = words[2].lower()
            currentTable = Table(FILE, currentDb)
            if words[3] == "where":
                whereAttr = words[4]
                relation = words[5]
                oldValue = words[6].replace('"', '')
                print("Deleting from " + words[2])
                currentTable.delete(whereAttr, relation, oldValue)

        elif words[0].lower() == "begin":
            if words[1].lower() == "transaction":
                if inTransaction:
                    print("!Error: Transaction already in progress")
                else:
                    print("Starting transaction")
                    inTransaction = True

        elif words[0].lower() == "commit":
            # Release lock
            for i, table in enumerate(locks):
                print("Releasing lock for table '" + table + "'")
                del locks[i]
                os.remove(DIRECTORY + "Locks/" + table + ".lock")
                currentTable = Table(memBuffer[i*2], currentDb)
                currentTable.writeTable(memBuffer[i*2 + 1])
            print("Ending transaction")
            inTransaction = False

        else:
            print("Invalid line: " + line)

# acquire_lock: this function creates the lock file for a transaction.
def acquire_lock (table):
    filePath = DIRECTORY + "Locks/" + table + ".lock"

    if not os.path.exists(filePath):
        lock = open(filePath, "w")
        lock.close()
        locks.append(table)
        return True
    else:
        return False

def db_exists (name):
    filePath = DIRECTORY + name + ""
    return os.path.exists(filePath)

def tb_exists(tname, currentDb):
    filePath = DIRECTORY + currentDb + "/" + tname + ".txt"
    return os.path.isfile(filePath)

if __name__ == "__main__":
    main()
