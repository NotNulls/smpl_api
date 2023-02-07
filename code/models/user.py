import sqlite3

class UserModel:

    def __init__(self, _id, username, password):
        #it is _id because the id is a python keyword
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # trailing comma tells python that we are creating a tuple
        row = result.fetchone()
        if row :
            #user = User(row[0],row[1],row[2])
            user = cls(*row) #passing it as a set of arguments
        else:
            user = None
        #no connection.commit() since we are not adding any data
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,)) # trailing comma tells python that we are creating a tuple
        row = result.fetchone()
        if row :
            #user = User(row[0],row[1],row[2])
            user = cls(*row) #passing it as a set of arguments
        else:
            user = None
        #no connection.commit() since we are not adding any data
        
        connection.close()
        return user