from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from kanban.database import db
from kanban.models import List

from kanban.api.errors import *

LIST_NAME_MAX_LENGTH = 25

output_fields = {
    'id': fields.Integer,
    'name': fields.String
}

list_parser = reqparse.RequestParser()
list_parser.add_argument('name', help='Name is required.', required=True)


class ListAPI(Resource):
    @jwt_required()
    @marshal_with(output_fields)
    def get(self, list_id=None):
        user_id = get_jwt_identity()

        if not list_id:
            return List.query.filter_by(user_id=user_id).all()

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        return existing_list

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        args = list_parser.parse_args()
        name = args.get('name')

        if len(name) > LIST_NAME_MAX_LENGTH:
            raise ListNameError()

        existing_list = List.query.filter_by(user_id=user_id).filter_by(name=name).first()

        if existing_list:
            raise ListAlreadyExistsError()

        new_list = List()
        new_list.user_id = user_id

        new_list.name = name

        db.session.add(new_list)
        db.session.commit()

        return {'message': 'List has been created.'}, 201

    @jwt_required()
    def put(self, list_id=None):
        user_id = get_jwt_identity()

        if not list_id:
            raise ListNotSpecifiedError()

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        args = list_parser.parse_args()
        name = args.get('name')

        if len(name) > LIST_NAME_MAX_LENGTH:
            raise ListNameError()

        existing_with_name = List.query.filter_by(user_id=user_id).filter_by(name=name).first()

        if existing_with_name:
            raise ListAlreadyExistsError()

        existing_list.name = name

        db.session.commit()

        return {'message': 'List has been updated.'}, 200

    @jwt_required()
    def delete(self, list_id=None):
        user_id = get_jwt_identity()

        if not list_id:
            raise ListNotSpecifiedError()

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        for card in existing_list.cards:
            db.session.delete(card)
        db.session.commit()

        db.session.delete(existing_list)
        db.session.commit()

        return {'message': 'List has been deleted.'}, 200
