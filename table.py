import os

class Table:
# should the table be a list of lists?????
    #constructor
    #declares the variables: tnme, db and filePath
    def __init__(self, tableName, db ):
        #print("In the table constructor")
        self.tname = tableName
        self.db = db #name of the database the table is located in
        self.filePath = "PA1/"+self.db+"/"+self.tname+".txt"


    #Creates the file that will represent the table
    def create(self):
        #filePath= "PA1/"+self.db+"/"+self.tname+".txt"
        open(self.filePath,"a+")
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
