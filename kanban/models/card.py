from kanban.database import db
from sqlalchemy.sql import func
from datetime import date


def update_completed_date(context):
    if 'completed' in context.get_current_parameters():
        completed = context.get_current_parameters()['completed']
        completed_on = context.get_current_parameters()['completed_on']

        if completed_on is None and completed:
            context.get_current_parameters()['completed_on'] = date.today()

        elif completed_on and not completed:
            context.get_current_parameters()['completed_on'] = None


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(250), nullable=True)
    deadline = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=func.now())
    last_updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    completed_on = db.Column(db.Date, default=update_completed_date, onupdate=update_completed_date)

    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
