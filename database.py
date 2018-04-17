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

    #Inner_join is the function to deal with join functionality for PA3
    # This function takes 4 paramaters
    #   self: itself
    #   tableList: 
    #   condition: what condition will the join be done on
    #   joinType: the type of join inner or left outer
    def inner_join(self, tableList, condition, joinType):
        joinedTable = []
        joinedTable.append(tableList[0][1] + tableList[1][1]) # append attributes

        words = condition.split()
        if len(words) != 3:
            print("!Failed to select: invalid condition '" + condition + "'")
            return

        #attribute to be checked, condition operator, parameter to check against
        attr1 = words[0].split('.')
        attrOperator = words[1]
        attr2 = words[2].split('.')

        # temp debug output
        #print(" | <" + str(attr1) + " " + attrOperator + " " + str(attr2) + ">")

        ####Getting the tables#####
        table1 = tableList[0]
        table2 = tableList[1]
        table1attr = ""
        table2attr = ""

        if attr1[0].lower() == table1[0].lower():
            table1attr = attr1[1].lower()
            table2attr = attr2[1].lower()   # just assume the other attribute is valid because I'm lazy
        elif attr1[0].lower() == table2[0].lower():
            table2attr = attr1[1].lower()
            table1attr = attr2[1].lower()
        else:
            print("!Failed to select: could not match attributes to tables")

        # note that tablex[1] is the attribute list
        # also note that using tablex[1].index() doesn't work beacuse each attribute
        # is a string containing both the attribute name and attribute type

        table1attrIndex = self.find_attr_index(table1[1], table1attr)
        table2attrIndex = self.find_attr_index(table2[1], table2attr)

        # temp debug output
        #print(" | Attr1 index: " + str(table1attrIndex) +" attr2 index: " + str(table2attrIndex))



        # NESTED LOOP JOIN
        # PLEASE KEEP IN MIND:
        #   table[0]  : table name
        #   table[1]  : table attributes
        #   table[2:] : table tuples

        for tuple1 in table1[2:]: # (inner join, so choice of table is arbitrary)
            successfulMatch = False
            for tuple2 in table2[2:]:
                #if inner join
                if self.match(tuple1[table1attrIndex], attrOperator, tuple2[table2attrIndex]):
                    joinedTable.append(tuple1 + tuple2) # should be tuple1 UNION (tuple2 - table2attr)
                    successfulMatch = True

            #if the match wasn't succesful and the joinType
            #was an outer left join then add the tuples that
            #are part of the left table that didn't match
            if not successfulMatch:
                if(joinType == "l-outer"):
                    joinedTable.append(tuple1)


        return joinedTable


    # Converts a string operator into a python operator
    # and returns the result
    def match(self, left, operator, right):
        if operator == "!=":
            if left != right:
                return True
        elif operator == "=":
            if left == right:
                return True
        elif operator == "<":
            if float(left) < float(right):
                return True
        elif operator == ">":
            if float(left) > float(right):
                return True
        else:
            return "?"
        return False


    def find_attr_index(self, attributeList, findAttribute):
        for i, element in enumerate(attributeList):
            if element.split()[0].lower() == findAttribute.lower():
                return i
        return -1


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

    #    print("\n |----->\n |DATA PASSED TO SELECT FUNCTION:\n | Attributes:") # temp debug output
    #    for element in attributes:           # temp debug output
    #        print(" | <" + element + ">")    # temp debug output

        if len(attributes[0]) == 0:
            print("!Error: nothing to select")
            return

######### from statement #########
        tablePairs = [] # [tableName, tableVariable]
        for line in tables[1:]:
            tablePair = line.split()
            tablePairs.append(tablePair)

        tableList = [] # The grand monstrosity

        # for each table passed in
        for table in tablePairs: # append to unique table
            tableName = table[0].lower()
            tableVariable = table[1].lower()

            currentTable = Table(tableName, self.name)
            tableBuffer = []
            tableBuffer.append(tableVariable)

            tbFile = open(currentTable.filePath, "r")

            for line in tbFile:
                tableBuffer.append(line.split("|")[:-1])

            tableList.append(tableBuffer)

        # tableList is now a list containing lists which contain a list name and more lists


        # The join function should now be called
        # it should return joinedTable, the result
        # of the join operation

    #    if tables[0] == "inner":
        joinedTable = self.inner_join(tableList, conditions[0], tables[0])
    #    else:
    #        print("NON INNER JOINS CURRENTLY NOT IMPLEMENTED")
    #        return


######### select statement #########
        # this should be rewritten to be more efficient
        # (just print selected rows, don't delete non-
        # selected then print remaining table)

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
