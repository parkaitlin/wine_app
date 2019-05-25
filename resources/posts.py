from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)
import models

post_fields = {
    'id': fields.Integer,
    'posted_by': fields.String,
    'name': fields.String,
    'vintage': fields.Integer,
    'review': fields.String,
}

class PostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'posted_by',
            required=False,
            help='username is required to post',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'name',
            required=False,
            help='Name of wine is required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'vintage',
            required=False,
            help='No vintage year was provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'review',
            required=False,
            help='No review/comment',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        posts = [marshal(post, post_fields) for post in models.Post.select()]
        return posts

    @marshal_with(post_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, "<---- args (req.body)")
        post = models.Post.create(**args)
        return post

posts_api = Blueprint('resources.posts', __name__)
api = Api(posts_api)
api.add_resource(
    PostList,
    '/posts',
    endpoint='posts'
)