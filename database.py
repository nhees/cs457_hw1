
import os

class Database:
#Functions

    #Constructor
    def __init__(self, dbName ):
    #Variables
        self.name = dbName
        self.tableNames = [] # our array
        self.create()
        #print("In database constructor")

    def create(self):
        filePath = "PA1/"+ self.name+""
        #checks if the directory already exists
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            #do we need to write a metafile???
    #    else:
    #    print("Database already exists2")


    def drop(self):
        filepath = "PA1/"+self.name+""
        os.system("rm -rf " + filepath)
        #creating the directory to represent the database
        #print("creating a database with the name "+ self.name +" ")
        #create a folder/ file database metadata
            # __name__table names/
            #metadata for all filestT
#####os.system
