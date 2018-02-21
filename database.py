
import os

class Database:
#Functions

    #Constructor
    def __init__(self, dbName ):
    #Variables
        self.name = dbName
        self.tableNames = [] # our array
        self.create()

#Create: This functions creates the folder that is representative of the
#Database
    #it will only create the folder if the
    def create(self):
        filePath = "PA1/"+ self.name+""
        #checks if the directory already exists
        if not os.path.exists(filePath):
            os.makedirs(filePath)

#Drop: this function is in charge of deleting the folder that represents the databse
    def drop(self):
        filepath = "PA1/"+self.name+""
        os.system("rm -rf " + filepath)
