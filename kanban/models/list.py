from kanban.database import db


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    cards = db.relationship('Card', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
