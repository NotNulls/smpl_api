import sqlite3
from flask_restful import Resource
from flask_restful import reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This cannot be left empty"  
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This cannot be left empty"
    )


    def post(self):
        data = UserRegister.parser.parse_args()

        #needs to be outside the connection othervise if there is no user, the connection would never close.
        if UserModel.find_by_username(data['username']):
            return {'message':'The user with that username already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()
