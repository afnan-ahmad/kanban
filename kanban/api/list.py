from flask_restful import Resource, fields, marshal_with, marshal, reqparse
from flask_security import auth_required, current_user

from kanban.database import db
from kanban.models import List

from kanban.api import card as card_api
from kanban.api.errors import *

LIST_NAME_MAX_LENGTH = 25

output_fields = {
    'id': fields.Integer,
    'name': fields.String
}

output_fields_with_card = {
    'id': fields.Integer,
    'name': fields.String,
    'cards': fields.Nested(card_api.output_fields)
}

list_parser = reqparse.RequestParser()
list_parser.add_argument('name', help='Name is required.', required=True)


class ListAPI(Resource):
    @auth_required('token')
    def get(self, list_id=None):
        user_id = current_user.id

        if not list_id:
            return marshal(List.query.filter_by(user_id=user_id).all(), output_fields)

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        return marshal(existing_list, output_fields_with_card)

    @auth_required('token')
    @marshal_with(output_fields)
    def post(self):
        user_id = current_user.id

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

        return new_list, 201

    @auth_required('token')
    def put(self, list_id=None):
        user_id = current_user.id

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

    @auth_required('token')
    def delete(self, list_id=None):
        user_id = current_user.id

        if not list_id:
            raise ListNotSpecifiedError()

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        query_parser = reqparse.RequestParser()
        query_parser.add_argument('move_to', type=int, location='args')

        query = query_parser.parse_args()
        move_to = query.move_to

        if move_to and move_to > -1:
            move_to_list = List.query.with_parent(current_user).filter_by(id=move_to).first()

            for card in existing_list.cards:
                card.list_id = move_to_list.id
            db.session.commit()

        else:
            for card in existing_list.cards:
                db.session.delete(card)
                db.session.commit()

        db.session.delete(existing_list)
        db.session.commit()

        return {'message': 'List has been deleted.'}, 200
