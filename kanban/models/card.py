from kanban.database import db
from sqlalchemy.sql import func


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)
    deadline = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=func.now())
    last_updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
