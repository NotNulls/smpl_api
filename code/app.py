from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from security import authenticate, identity
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "emmanuel"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#this automatically creates a /auth
jwt = JWT(app, authenticate, identity)


#API works with resources and each resource is going to be represented by a class

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True, ssl_contex=('cert.pem','key.pem'))


