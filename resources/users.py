import json

from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)

from flask_login import login_user, logout_user, login_required, current_user

from flask_bcrypt import check_password_hash

import models

user_fields = {
    'username': fields.String,
    'id': fields.Integer
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            print(args, ' this is args')
            user = models.User.create_user(**args)
            login_user(user)
            create_user = marshal(user, user_fields)
            return make_response(
                json.dumps({
                    "user": create_user 
                }), 201)
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400) 


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        super().__init__()    
    
    def post(self):
        try:
            args = self.reqparse.parse_args()
            user = models.User.get(models.User.username==args['username'])
            if(user):
                print(user, "this is user")
                if(check_password_hash(user.password, args['password'])):
                    return make_response(
                        json.dumps({
                            'user': marshal(user, user_fields),
                            'message': 'success'
                        }), 200)
                else:
                    return make_response(
                        json.dumps({
                            'message':"incorrect password"
                        }), 401)
        except models.User.DoesNotExist:
            return make_response(
                    json.dumps({
                        'message':"Username does not exist"
                    }), 400)

class SingleUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=False,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=False,
            help='No password provided',
            location=['form', 'json']
        )
        super().__init__()
        
    @marshal_with(user_fields)
    def put(self, id):
      args = self.reqparse.parse_args()
      print(args, 'this is args')
      query = models.User.update(**args).where(models.User.id==id)
      query.execute()
      return(models.User.get(models.User.id==id), 200)



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/registration'
)

api.add_resource(
    User,
    '/login'
)

api.add_resource(
    SingleUser,
    '/<int:id>'
)