from kanban.database import db
from flask_security import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)

    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    lists = db.relationship('List', lazy=True)
