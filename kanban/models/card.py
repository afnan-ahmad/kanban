from kanban.database import Base

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
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


class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    title = Column(String(25), nullable=False)
    content = Column(String(250), nullable=True)
    deadline = Column(Date, nullable=False)
    completed = Column(Boolean)

    created_at = Column(DateTime, default=func.now())
    last_updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    completed_on = Column(Date, default=update_completed_date, onupdate=update_completed_date)

    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
