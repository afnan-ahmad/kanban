from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from kanban.models import List, Card

from kanban.api.errors import *

from datetime import date


class SummaryAPI(Resource):
    @jwt_required()
    def get(self, list_id=None):
        user_id = get_jwt_identity()

        if not list_id:
            return {'total_lists': List.query.filter_by(user_id=user_id).count()}

        existing_list = List.query.filter_by(user_id=user_id).filter_by(id=list_id).first()

        if not existing_list:
            raise ListNotFoundError()

        total_count = len(existing_list.cards)

        completed_count = Card.query.with_parent(existing_list).filter_by(completed=True).count()
        overdue_count = Card.query.with_parent(existing_list).filter_by(completed=False).filter(
            Card.deadline < date.today()).count()

        return {
            'id': existing_list.id,
            'name': existing_list.name,
            'total': total_count,
            'completed': completed_count,
            'overdue': overdue_count
        }
