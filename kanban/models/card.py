from kanban.database import db


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)
    deadline = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean)

    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
