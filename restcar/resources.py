#!/usr/bin/env python

from flask import abort, g, Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, marshal_with, fields

from restcar.models import User
from restcar.extensions import auth, db

__version__ = '1'

api_blueprint = Blueprint("api", __name__, url_prefix='/api/v{}'.format(__version__))
api = Api(api_blueprint)


class UserResource(Resource):
    """Endpoint for User Creation
    """
    def __init__(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument('email', required=True)
        user_parser.add_argument('password')
        self.parser = user_parser

    def post(self):
        args = self.parser.parse_args()
        instance = User(**args)
        db.session.add(instance)
        db.session.commit()
        return {"msg": "User {} added, check your e-mail for the activation link.".format(instance.email)}

api.add_resource(UserResource, '/users/')


class UserActivationResource(Resource):
    def get(self, email):
        user = User.get_by_email(email)
        if user.active:
            msg = {'msg': 'User is already active.'}
        else:
            user.activate()
            msg = {'msg': 'User {} activated successfully'.format(email)}
        return msg

api.add_resource(UserActivationResource, '/users/<email>/activate')


class RestrictedResource(Resource):
    """
    Resource only available to activated users
    """
    @auth.login_required
    def get(self):
        return {"allowed": "You shall pass!"}

api.add_resource(RestrictedResource, '/restricted')
