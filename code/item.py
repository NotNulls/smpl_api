from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from flask import request
import json

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required = True,
        help = 'Cannot be left blank.'
    )
    #It is going to parse the arguments that come trough JSON payload and it is going to put the valid ones in data. We added only price argument so that is the only one that can get changed.
    

    #in production environment it is wise to put on all of the methods
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return  {'message':'Item not on a list'}, 404

           

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE NAME=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return{'item': {'name':row[0], 'price':row[1]}}

    def post(self, name):

        #error first approach. No point in loading data first if there is a name in our database
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        self.insert(item)

        try:
            self.insert(item)
        except:
            return {'message':'An error occured inserting the item'}

        return item, 500 #internal server error
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items values (?,?)"

        cursor.execute(query,(item['name'], item['price']))
        
        connection.commit()
        connection.close()


    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"

        cursor.execute(query,(name,))
        
        connection.commit()
        connection.close()

        return {'message':'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name':name, 'price':data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message':'An error occure inserting the item.'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message':'An error occured updating the item.'}, 500
        return updated_item

    @classmethod
    def updated(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"

        cursor.execute(query,(item['price'],item['name']))
        
        connection.commit()
        connection.close()

        return 

class ItemList(Resource):
    def get(self):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM items')
        items = dict(cursor.fetchall())
        connect.close()
        return  {'items':items}