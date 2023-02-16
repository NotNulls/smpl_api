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
    parser.add_argument(
        'store_id',
        type=int,
        required = True,
        help = 'Every needs to be assigned to a store.'
    )

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
        item = ItemModel(name, data['price'], data['store_id'])
        #alternatively we could do the following
        # item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message':'An error occured inserting the item'}

        return item, 500 #internal server error


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted.'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            item.price = data['price']
        item.save_to_db()
        return item.json()
    

class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}
        #return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))}
