from kanban.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class List(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)

    cards = relationship('Card', lazy=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
