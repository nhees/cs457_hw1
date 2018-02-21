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
    def select(self):
        print("selecting the table")
            #print the table info
                # print whatever is in the datafile

#alters the table information
    def alter(self):
        print("altering the table")
        # alter the metadata???/ data

#adds and attribute to the table
    def add_column(self,type, name, length):

        file = open(self.filePath,"a")

        if(type == int):
            file.write("| "+name +" int")
        elif(type == float):
            file.write("| "+name+" float")
        elif(type == "char"):
            file.write("| " +name+ " char("+ length +")")
        else:
            file.write("| " + name + " varchar("+length+")")
