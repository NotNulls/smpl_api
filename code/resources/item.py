from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from flask import request
import json
from models.item import ItemModel


class Item(Resource):
    #Resource is mapping the api endpoints
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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return  {'message':'Item not on a list'}, 404


    def post(self, name):

        #error first approach. No point in loading data first if there is a name in our database
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        data = request.get_json()
        item = ItemModel(name, data['price'])
        ItemModel.insert(item)

        try:
            item.insert()
        except:
            return {'message':'An error occured inserting the item'}

        return item, 500 #internal server error


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

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message':'An error occure inserting the item.'}, 500
        else:
            try:
                updated_item.updated()
            except:
                return {'message':'An error occured updating the item.'}, 500
        return updated_item.json()
    

class ItemList(Resource):
    def get(self):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM items')
        items = dict(cursor.fetchall())
        connect.close()
        return  {'items':items}
    
