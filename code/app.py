from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from security import authenticate, identity
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "emanuel"
api = Api(app)

#this automatically creates a /auth
jwt = JWT(app, authenticate, identity)


#API works with resources and each resource is going to be represented by a class

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(debug=True)
    

