from kanban.database import Base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from flask_security import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String, nullable=False)
    active = Column(Boolean)

    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))
    lists = relationship('List', lazy=True)
