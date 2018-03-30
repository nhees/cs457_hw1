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

    def inner_join(self, tableList, condition):

        words = condition.split()
        if len(words) != 3:
            print("!Failed to select: invalid condition '" + condition + "'")
            return

        #attribute to be checked, condition operator, parameter to check against
        table1attr = words[0].split('.')
        condOperator = words[1]
        table2attr = words[2].split('.')

        # temp debug output
        print(" | <" + str(table1attr) + " " + condOperator + " " + str(table2attr) + ">")
        ####Getting the tables#####
        table1 = tableList[0]
        table2 = tableList[1]

        for ind in table1:
            if table1attr in ind:
                attr1Index = table1.index(i)

        for ind in table2:
            if table2attr in ind:
                attr2Index = table2.index(i)

        print("Attr1 index:" +attr1Index+" attr2 index:" + attr2Index+" ")
        #attrIndex = 0
        #for attribute in joinedTable[0]:
            #find condition attribute
        #    attrName = attribute.split()[0]
        #    if attrName == table1attr[0]:
                #attr index has been found, stop looking
        #        break
        #    attrIndex += 1
        #if attrIndex == len(joinedTable[0]):
            #attr wasn't found
        #    print(" |<-----\n") # temp debug output
        #    print("!Failed to select: couldn't apply constraint to attribute '"
        #          + table1attr[0] + "'")
        #    return

        #remove rows from that don't match condition from table being printed
        if condOperator == "!=":
            for row in joinedTable[1:]:
                if row[attrIndex] == table2attr[0]:
                    joinedTable.remove(row)
        elif condOperator == "=":
            for row in joinedTable[1:]:
                if row[attrIndex] != table2attr[0]:
                    joinedTable.remove(row)
        elif condOperator == "<":
            for row in joinedTable[1:]:
                if float(row[attrIndex]) >= float(table2attr[0]):
                    joinedTable.remove(row)
        elif condOperator == ">":
            for row in joinedTable[1:]:
                if float(row[attrIndex]) <= float(table2attr[0]):
                    joinedTable.remove(row)
        else:
            print("!Failed to select: unknown operator '" + condOperator + "'")
            return

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
        tablePairs = [] # [tableName, tableVariable]
        for line in tables[1:]:
            tablePair = line.split()
            tablePairs.append(tablePair)

        tableList = []

        # for each table passed in
        for table in tablePairs: # append to unique table
            tableName = table[0].lower()
            tableVariable = table[1].lower()

            currentTable = Table(tableName, self.name)
            tableBuffer = []
            tbFile = open(currentTable.filePath, "r")

            for line in tbFile:
                tableBuffer.append(line.split("|")[:-1])

            tableList.append(tableBuffer)

        # tableList is now a list of list of lists

        print(" | Table:\n | Join type: " + tables[0]) # temp debug output
        print(" | " + str(tableList))                   # temp debug output
        print(" | Conditions:")                         # temp debug output

        # The join function should now be called
        # it should return joinedTable, the result
        # of the join operation

######### where statement #########
#        for condition in conditions:
#            words = condition.split()
#            if len(words) != 3:
#                print("!Failed to select: invalid condition '" + condition + "'")
#                return

            #attribute to be checked, condition operator, parameter to check against
#            condAttrPair = words[0].split('.')
#            condOperator = words[1]
#            condParamPair = words[2].split('.')

            # temp debug output
#            print(" | <" + str(condAttrPair) + " " + condOperator + " " + str(condParamPair) + ">")

#            attrIndex = 0
#            for attribute in joinedTable[0]:
                #find condition attribute
#                attrName = attribute.split()[0]
#                if attrName == condAttrPair[0]:
                    #attr index has been found, stop looking
#                    break
#                attrIndex += 1
#            if attrIndex == len(joinedTable[0]):
                #attr wasn't found
#                print(" |<-----\n") # temp debug output
#                print("!Failed to select: couldn't apply constraint to attribute '"
#                      + condAttrPair[0] + "'")
#                return

            #remove rows from that don't match condition from table being printed
#            if condOperator == "!=":
#                for row in joinedTable[1:]:
#                    if row[attrIndex] == condParamPair[0]:
#                        joinedTable.remove(row)
#            elif condOperator == "=":
#                for row in joinedTable[1:]:
#                    if row[attrIndex] != condParamPair[0]:
#                        joinedTable.remove(row)
#            elif condOperator == "<":
#                for row in joinedTable[1:]:
#                    if float(row[attrIndex]) >= float(condParamPair[0]):
#                        joinedTable.remove(row)
#            elif condOperator == ">":
#                for row in joinedTable[1:]:
#                    if float(row[attrIndex]) <= float(condParamPair[0]):
#                        joinedTable.remove(row)
#            else:
#                print("!Failed to select: unknown operator '" + condOperator + "'")
#                return

        print(" |<-----\n") # temp debug output

######### select statement #########
        # this should be rewritten to be more efficient
        # (just print selected rows, don't delete non-
        #  selected then print remaining table)

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
