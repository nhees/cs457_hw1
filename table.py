import os

DIRECTORY = "PA4/"

class Table:
# Handles table operations
# Initialized with a table name, can perform various operations on the table

    #constructor
    #declares the variables: tnme, db and filePath
    def __init__(self, tableName, db ):
        self.tname = tableName
        self.db = db #name of the database the table is located in
        self.filePath = DIRECTORY + self.db + "/" + self.tname + ".txt"

    #Creates the file that will represent the table
    def create(self):
        #filePath= "PA1/"+self.db+"/"+self.tname+".txt"
        open(self.filePath,"a")
        #print("create the table")

    #deletes the table file
    def drop(self):
        os.remove(self.filePath)

    # update: changes an attributes value for specific tuples
    # param arguments:
    #       where attribute and needed value as well as attribute to change and new value
    # algorithm:
    #     Ensure that the tuple meets the where clause requirments
    #     if the clause requirements are met then the set attribute
    #     value is changed in that tuple
    def update(self, setAttr, newValue, whereAttr, oldValue, inTransaction, table):

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
        if inTransaction:
            #table.append(self.tname)
            tablelines = tbFile.readlines()
            tablecontent= tbFile.readlines()

            for line in tablelines:
                templine = line.split("|")
                if oldValue == templine[whereAttrIndex].strip("''"):
                    templine[whereAttrIndex] = newValue
                tablecontent.append(templine)

            table.append(tablecontent)
            print (str(table))

            #get a variable to hold table name and contents
            #NEED TO LOAD TO TABLE
        else: #if not in transaction mode proceed normally
            lines = tbFile.readlines()
            tbFile.seek(0)
            tbFile.truncate()

            #rewriting the metadata line
            tbFile.write(testmetaData)

            for line in lines:
                    testline = line.split("|")
                    if oldValue == testline[whereAttrIndex].strip("''"):
                        line = line.replace(testline[setAttrIndex].strip("''"), newValue)
                    tbFile.write(line)


    # Delete: Deletes a tuple to the table
    # param arguments:
    #       attribute information the tuple must have to be deleted
    # algorithm:
    #     Reads through every tuple to ensure that it has the attribute relation
    #     requirements to be deleted from the table
    def delete(self, attribute,relation, value):
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

        #rewriting themetaData line
        tbFile.write(testmetaData)

        for line in lines:
                testline = line.split("|")

                if relation == '=':
                    if testline[attrIndex].strip("''") != value.strip("''"):
                        tbFile.write(line)
                elif relation == '<':
                    if float(testline[attrIndex]) > float(value):
                        tbFile.write(line)
                else:
                    if float(testline[attrIndex]) < float(value):
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
            print("Invalid tuple length: " + str(len(arguments))
                  + " (there are " + str(len(attributes) - 1) + " attributes)")
            successfulInsert = False
        else:
            for i, arg in enumerate(arguments):
                #select attribute type
                currentType = attributes[i].split()[1]

                data = str
                if currentType == "int":
                    #float conversion allows truncation if needed (e.g. 14.43 -> 14)
                    data = str(int(float(arg)))
                elif currentType == "float":
                    data = str(float(arg))
                elif currentType.split("(")[0] == "varchar" or currentType.split("(")[0] == "char":
                    # enforce quotation marks around char
                    if len(arg) < 2 or \
                            ((arg[0] != "'" or arg[-1] != "'") \
                              and (arg[0] != '"' or arg[-1] != '"')):
                        print("!Error: No quotation marks around char/varchar: " + arg)
                        return
                    else:
                        string = arg[1:-1]
                        #extract var/char length
                        if currentType.split("(")[0] == "varchar":
                            length = int(currentType.split(")")[0][8:])
                        else:
                            length = int(currentType.split(")")[0][5:])

                        #cut input to max length of var/char
                        data = "'" + string[0:length] + "'"

                dataToAdd += data + "|"

            wrFile = open(self.filePath, "a")
            wrFile.write(dataToAdd)

        return successfulInsert

    #adds and attribute to the table
    def add_column(self,type, name, length):

        file = open(self.filePath,"a")

        if(type == int):
            file.write(name + " int" + "|")
        elif(type == float):
            file.write(name + " float" + "|")
        elif(type == "char"):
            file.write(name + " char(" + length + ")" + "|")
        else:
            file.write(name + " varchar(" + length + ")" + "|")
