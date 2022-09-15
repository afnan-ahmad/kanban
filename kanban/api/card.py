from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from kanban.database import db
from kanban.models import Card, List

from kanban.api.errors import *

import datetime

CARD_TITLE_MAX_LENGTH = 25
CARD_CONTENT_MAX_LENGTH = 250


class DateTimeFormat(fields.Raw):
    def format(self, value):
        if type(value) is datetime.date:
            return datetime.datetime(value.year, value.month, value.day, 0, 0, 0).isoformat()
        elif type(value) is datetime.datetime:
            return value.isoformat()


output_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'deadline': DateTimeFormat,
    'completed': fields.Boolean,
    'created_at': DateTimeFormat,
    'last_updated_at': DateTimeFormat,
    'completed_on': DateTimeFormat,
    'list_id': fields.Integer
}

card_parser = reqparse.RequestParser()
card_parser.add_argument('list_id', type=int, help='List ID is required.', required=True)
card_parser.add_argument('title', help='Title is required.', required=True)
card_parser.add_argument('content')
card_parser.add_argument('deadline', type=lambda x: datetime.date.fromisoformat(x),
                         help='Deadline is required.', required=True)
card_parser.add_argument('completed', type=bool)


class CardAPI(Resource):
    @jwt_required()
    @marshal_with(output_fields)
    def get(self, card_id=None):
        user_id = get_jwt_identity()

        if not card_id:
            return Card.query.filter_by(user_id=user_id).all()

        card = Card.query.filter_by(user_id=user_id).filter_by(id=card_id).first()

        if not card:
            raise CardNotFoundError()

        return card

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        args = card_parser.parse_args()
        title = args.get('title')

        if len(title) > CARD_TITLE_MAX_LENGTH:
            raise CardTitleError()

        content = args.get('content')

        if len(content) > CARD_CONTENT_MAX_LENGTH:
            raise CardContentError()

        deadline = args.get('deadline')
        completed = args.get('completed')
        list_id = args.get('list_id')

        if deadline < datetime.date.today() and not completed:
            raise CardPastDeadlineError()

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        card = Card()
        card.user_id = user_id

        card.title = title
        card.content = content
        card.deadline = deadline
        card.completed = completed

        existing_list.cards.append(card)

        db.session.commit()

        return {'message': 'Card has been created.'}, 201

    @jwt_required()
    def put(self, card_id=None):
        user_id = get_jwt_identity()

        if not card_id:
            raise CardNotSpecifiedError()

        card = Card.query.filter_by(user_id=user_id).filter_by(id=card_id).first()

        if not card:
            raise CardNotFoundError()

        card_parser_update = card_parser.copy()
        card_parser_update.replace_argument('list_id', type=int, default=card.list_id)
        card_parser_update.replace_argument('title', default=card.title)
        card_parser_update.replace_argument('content', default=card.content)
        card_parser_update.replace_argument('deadline', type=lambda x: datetime.date.fromisoformat(x),
                                            default=card.deadline)
        card_parser_update.replace_argument('completed', type=bool, default=card.completed)

        args = card_parser_update.parse_args()
        title = args.get('title')

        if len(title) > CARD_TITLE_MAX_LENGTH:
            raise CardTitleError()

        content = args.get('content')

        if len(content) > CARD_CONTENT_MAX_LENGTH:
            raise CardContentError()

        deadline = args.get('deadline')
        completed = args.get('completed')
        list_id = args.get('list_id')

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        card.list_id = existing_list.id

        card.title = title
        card.content = content
        card.deadline = deadline
        card.completed = completed

        db.session.commit()

        return {'message': 'Card has been updated.'}, 200

    @jwt_required()
    def delete(self, card_id=None):
        user_id = get_jwt_identity()

        if not card_id:
            raise CardNotSpecifiedError()

        card = Card.query.filter_by(user_id=user_id).filter_by(id=card_id).first()

        if not card:
            raise CardNotFoundError()

        db.session.delete(card)
        db.session.commit()

        return {'message': 'Card has been deleted.'}, 200
