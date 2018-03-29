import os
from table import Table

DIRECTORY = "PA3/"

class Database:
# Creates and Destroys databases
# Initialized with a database name

    #Functions
    #Constructor
    def __init__(self, dbName ):
        #Variables
        self.name = dbName
        self.tableNames = []
        self.create()

    #Create: This functions creates the folder that is representative of the
    #database. It will only create the folder if the directory does not
    #already exist
    def create(self):
        filePath = DIRECTORY + self.name + ""
        #checks if the directory already exists
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    #Drop: this function is in charge of deleting the folder that represents the databse
    def drop(self):
        filepath = DIRECTORY + self.name + ""
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

        print("\n |----->\n |DATA PASSED TO SELECT FUNCTION:\n | Attributes:") # temp debug output
        for element in attributes:           # temp debug output
            print(" | <" + element + ">")    # temp debug output

        if len(attributes[0]) == 0:
            print("!Error: nothing to select")
            return

######### from statement #########
        tablePairs = []
        for line in tables[1:]:
            tablePair = line.split()
            tablePairs.append(tablePair)

        #just use first table for now
        currentTable = Table(tablePairs[0][0].lower().split()[0], self.name)
        tbFile = open(currentTable.filePath, "r")

        for line in tbFile:
            joinedTable.append(line.split("|")[:-1])

        print(" | Tables:\n | Join type: " + tables[0])   # temp debug output
        for element in tablePairs:                        # temp debug output
            print(" | <" + str(element) + ">")            # temp debug output
        print(" | Conditions:")                           # temp debug output

######### where statement #########
        for condition in conditions:
            words = condition.split()
            if len(words) != 3:
                print("!Failed to select: invalid condition '" + condition + "'")
                return

            #attribute to be checked, condition operator, parameter to check against
            condAttrPair = words[0].split('.')
            condOperator = words[1]
            condParamPair = words[2].split('.')

            # temp debug output
            print(" | <" + str(condAttrPair) + " " + condOperator + " " + str(condParamPair) + ">")

            attrIndex = 0
            for attribute in joinedTable[0]:
                #find condition attribute
                attrName = attribute.split()[0]
                if attrName == condAttrPair[0]:
                    #attr index has been found, stop looking
                    break
                attrIndex += 1
            if attrIndex == len(joinedTable[0]):
                #attr wasn't found
                print(" |<-----\n") # temp debug output
                print("!Failed to select: couldn't apply constraint to attribute '"
                      + condAttrPair[0] + "'")
                return

            #remove rows from that don't match condition from table being printed
            if condOperator == "!=":
                for row in joinedTable[1:]:
                    if row[attrIndex] == condParamPair[0]:
                        joinedTable.remove(row)
            elif condOperator == "=":
                for row in joinedTable[1:]:
                    if row[attrIndex] != condParamPair[0]:
                        joinedTable.remove(row)
            elif condOperator == "<":
                for row in joinedTable[1:]:
                    if float(row[attrIndex]) >= float(condParamPair[0]):
                        joinedTable.remove(row)
            elif condOperator == ">":
                for row in joinedTable[1:]:
                    if float(row[attrIndex]) <= float(condParamPair[0]):
                        joinedTable.remove(row)
            else:
                print("!Failed to select: unknown operator '" + condOperator + "'")
                return

        print(" |<-----\n") # temp debug output

######### select statement #########
        for i, attribute in enumerate(joinedTable[0]):
            attrName = attribute.split()[0]
            if "*" not in attributes and attrName not in attributes:
                for row in joinedTable:
                    #remove the whole column if it isn't selected
                    row.pop(i)

        # print result
        for row in joinedTable:
            rowText = "| "
            for item in row:
                rowText += item + " | "
            print(rowText)
