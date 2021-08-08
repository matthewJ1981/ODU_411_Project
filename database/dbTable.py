import mysql.connector
from dbConnect import dbConnect
import pdb
from abc import ABC, abstractmethod


class Table(ABC):
    """
    Base table class for modulating queries

    """
    def __init__(self, cnx, tableName, unmutables, primaryKey, foreignKey):
        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.tableName = tableName
        self.unmutables = unmutables
        self.primaryKey = primaryKey
        self.foreignKey = foreignKey

    #Add tuple to database
    #Parameters - query in the form of an insert statement and values to be included in the statement
    #Return  - void but throws exception 
    def add(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.addUpdate()
        except mysql.connector.Error as err:
            # print("Error in table add")
            print(err)
            # print(query)
            # print(values)
            raise
        
        self.cnx.commit() 

    #Add entry to hasUpdate table to signal something in the database has changed
    def addUpdate(self):
        #print("Add update")
        # def convert(_type):
        #     if _type == "<class 'dbBubble.Bubble'>":
        #         return "bubble"
        def convert(s):
            return s[s.find('.') + 1: len(s) - 2]
        
        s = convert(str(self.__class__))
        #print(s)

            # elif _type == "<class 'dbParent.Parent'>":
            # if str(self.__class__) == "<class 'dbBubble.Bubble'>":
            #     print("Bubble")
        try:
            self.cursor.execute("INSERT INTO hasUpdate (tab, child, parent) VALUES (%s, %s, %s)", (s, 1, 1))
        except mysql.connector.Error as err:
            #print(err)
            pass

        self.cnx.commit() 

    #Remove entry in database after update has been pulled to the local data structure
    def remUpdate(self, table, user):
        
        #Query template
        def exec(query, values, res):
            #print(query)
            #print(values)
            try:
                self.cursor.execute(query, values)
            except mysql.connector.Error as err:
                #print(err)
                raise
            if res:
                res = self.cursor.fetchone()
                self.cnx.commit() 
                return res

        #Delete row or entire table
        def delete(table = None):
            query = "DELETE FROM hasUpdate WHERE tab = %s"
            values = (table,)
            #print(query)
            #print(values)
            if table == None:
                query = "DELETE FROM hasUpdate"
                values = ()
            try:
                self.cursor.execute(query, values)
            except mysql.connector.Error as err:
                print(err)
                raise
            self.cnx.commit() 

        #If no table or user is provided, delete entire table
        if table == None or user == None:
            delete()
            
        else:
            # Set user flag to 0
            query = "UPDATE hasUpdate SET " + user + " = 0 WHERE tab = %s"
            values = (table,)
            exec(query, values, False)

            # if both user flags are 0, delete the row from the table
            query = ("SELECT child, parent FROM hasUpdate where tab = %s")
            values = (table,)
            ready = exec(query, values, True)
            if ready != None and ready[0] == 0 and ready[1] == 0:
                delete(table)

        

    def getUpdate(self):
        #print("getUpdate")
        try:
            self.cursor.execute("select * from hasUpdate")
            res = self.cursor.fetchall() 
            #print("result " + str(res))
            #return self.cursor.fetchall()
            self.cnx.commit() 
            return res
        except mysql.connector.Error as err:
            print(err)
            raise

    #Remove tuple by ID
    #Parameters - tuple id
    #Return - returns true unless exception is thrown   
    def remove(self, id):
        return self.removeAll(("id",), (id,))

    #Remove all tuples matching where clause.  Default removes all tuples
    #Parameters - optional where fields
    #Return - returns true unless exception is thrown
    def removeAll(self, whereFields = (), values = ()):
        query = "DELETE FROM " + self.tableName + " " + self.whereClause(whereFields)
        # print(query)
        # print(values)
        try:
            self.cursor.execute(query, values)
            self.addUpdate()
        except Exception as e:
            print(e)
            return False

        self.cnx.commit()

        return True
    
    #Update one field for a specific tuple
    #Parameters - tuple id, field to be updated, and the new value
    #Return - returns true unless exception is thrown
    def setFieldByID(self, id, field, value):
        #print("setFieldByID")
        return self.setFieldsByID(id, (field,), (value,))

    #Update multiple fields for a specific tuple
    #Parameters - tuple id, fields to be updated, and the new values
    #Return - returns true unless exception is thrown
    def setFieldsByID(self, id, fields, values):
        #print("setFieldsByID")
        return self.setFields(fields, values, ("id",), (id,)  )

    #Update one field for a all tuples
    #Parameters - field to be updated, and the new value
    #Return - returns true unless exception is thrown
    def setField(self, field, value):
        #print("setField")
        return self.setFields( (field,), (value,) )

    #Update multiple fields for all tuples
    #Parameters - fields to be updated, new values, optional where fields and values
    #Return - returns true unless exception is thrown
    def setFields(self, setFields, setValues = (), whereFields = (), whereValues = ()):
        #print("SetFields")
        for field in setFields:
            if field in self.unmutables:
                print("Cannot update this field")
                return False
        try:
            query = "UPDATE " + self.tableName  + " " + self.setClause(setFields) + " " + self.whereClause(whereFields)
            values = setValues + whereValues
            # print(query)
            # print(values)
            self.cursor.execute(query, values)
            self.addUpdate()
 
        except mysql.connector.Error as err:
            print(err)
            return False

        self.cnx.commit()
        return True

    #Get ID of a tuple from primary key
    #Parameters - primary key as tuple
    #Return - returns id if tuple exists, else returns None type
    def getID(self, values):
        return self.getFirst(self.getField("id", self.primaryKey, values), True)
    
    #Get one field for specific tuple
    #Parameters - tuple id and required field name
    #Return - returns field if tuple exists, else returns None type
    def getFieldByID(self, id, field):
        return self.getFirst(self.getFieldsByID(id, (field,)), True)

    #Get multiple fields for specific tuple
    #Parameters - tuple id and required fields
    #Return - returns fields as a tuple if record exists, else returns empty tuple
    def getFieldsByID(self, id, fields = ("*",)):
        return self.getFirst(self.getFields(fields, ("id",), (id,)), False)

    #Get one field for multiple tuples
    #Parameters - required field names and optional where fields and values
    #Return - returns list of tuples if record exists, else returns empty list
    def getField(self, field, whereFields = (), values = ()):
        temp = self.getFields((field,), whereFields, values)
        res = []
        for tup in temp:
            res.append(tup[0])
        
        return tuple(res)
        
    #Get multiple fields for multiple tuples
    #Parameters - tuple id and required fields
    #Return - returns fields as a tuple if record exists, else returns empty tuple
    def getFields(self, selectFields = ("*",), whereFields = (), values = ()):
        query = self.selectClause(selectFields) + " FROM " + self.tableName + " " + self.whereClause(whereFields)
        #print(query)
        try:
            self.cursor.execute(query, values)
        except Exception as e:
            print(e)
            return []

        result = self.cursor.fetchall()
        self.cnx.commit()
        return result

    #Get all fields in all tuples
    #Parameters - 
    #Return - returns all records as list of tuples
    def getAll(self):
        return self.getFields()

    #Return first entry in the tuple of the length is one instead of returning a tuple of length 1
    #Parameters - list or tuple returned from mysql connector and boolean value, set true for single object, false for tuple
    #Return - returns first object or tuple, unless original data was empty in which case this returns None or empty tuple
    def getFirst(self, data, single):
        if data == None or len(data) == 0:
            if single:
                return None
            else:
                return ()

        if len(data) > 1:
            raise Exception("In table.getFirst: Length of result is more than 1, possible loss of data")
        
        return data[0]
    
    #Get all table fields for a specific tuple by id
    #Parameters - tuple id
    #Return - all fields in tuple as python tuple
    def getByID(self, id):
        return self.getFieldsByID(id)

    #Clause helper
    #Parameters - fields to be included in the clause
    #Return - entire clause as string
    def selectClause(self, fields):
        return self.clause(fields, "SELECT ", ", ")

    #Clause helper
    #Parameters - fields to be included in the clause
    #Return - entire clause as string
    def setClause(self, fields):
        return self.clause(fields, "SET ", ", ")

    #Clause helper
    #Parameters - fields to be included in the clause
    #Return - entire clause as string
    def whereClause(self, fields):
        return self.clause(fields, "WHERE ", " AND ")

    #Construct clauses
    #Parameters - fields, type from helper, and delimiter
    #Return - entire clause as string
    def clause(self, fields, _type, delim):
        if len(fields) == 0:
            return ""

        clause = _type
        for value, field in enumerate(fields):
            clause += field
            if _type != "SELECT ":
                clause += " = %s"
            if value < len(fields) - 1:
                clause += delim
        return clause

    #Format date and time
    #Parameters - datetime object
    #Return - string in format M/D/Y H:M:S
    def formatDateTime(self, dateTime):
        return dateTime.strftime("%m/%d/%y %H:%M:%S")

if __name__ == "__main__":
    db = dbConnect('localhost')
    db.createTestDB()
    db.useDB()

    query = "INSERT INTO parent(username, password, email_addr, first_name, last_name) VALUES(%s, %s, %s, %s, %s)"
 
    table = Table(db.cnx(), "parent", ("id", "username"), ("username",), [])

    table.add(query, ("p1", "pw1", "e1", "f1", "l1"))
    table.add(query, ("p2", "pw2", "e2", "f2", "l1"))
    table.add(query, ("p3", "pw3", "e3", "f3", "l2"))
    id1 = table.getID(("p1",))
    id2 = table.getID(("p2",))
    id3 = table.getID(("p3",))
    print(table.removeAll(("password",), ("pw4",)))
    print("getFieldsByID(id):\t\t\t" +              str(table.getFieldsByID(id1)))
    print("getFieldByID(id, field):\t\t" +          str(table.getFieldByID(id1, "first_name"))) #  field
    print("getFieldsByID(id, fields):\t\t" +        str(table.getFieldsByID(id1, ("first_name",)))) # (field1, field2)
    print("getFields():\t\t\t\t" +                  str(table.getFields()))  # [(,),]
    print("getField(field):\t\t\t" +                str(table.getField("first_name"))) # (,)
    print("getFields(fields, where, value):\t" +    str(table.getFields(("first_name",), ("id",), (id1,))))
    db.close()