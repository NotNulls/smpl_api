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

        connectiton = sqlite3.connect('data.db')
        cursor = connectiton.cursor()

        #NULL goes for the autoincrementation of id which is a primary key
        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query,(data['username'],data['password'],))

        connectiton.commit()
        connectiton.close()

        return {'message':'User successfully created'}, 201
