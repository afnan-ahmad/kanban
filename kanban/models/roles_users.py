from kanban.database import Base

from sqlalchemy import Column, Integer, ForeignKey


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    role_id = Column('role_id', Integer, ForeignKey('role.id'))
