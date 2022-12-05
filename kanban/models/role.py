from kanban.database import Base

from sqlalchemy import Column, Integer, String

from flask_security import RoleMixin


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))
