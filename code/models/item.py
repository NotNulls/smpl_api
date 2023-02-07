import sqlite3

class ItemModel():
    def __init__(self,name, price) -> None:
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE NAME=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            #returns object of class ItemModel
            return cls(*row)
        
    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items values (?,?)"

        cursor.execute(query,(self.name, self.price))
        
        connection.commit()
        connection.close()

    def updated(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"

        cursor.execute(query,(self.name, self.price))
        
        connection.commit()
        connection.close()

        