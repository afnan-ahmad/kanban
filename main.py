import os
from kanban import app, config
from kanban.database import db
from kanban.models import User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from kanban.forms import KanbanRegisterForm

if os.getenv('ENV', 'development') == 'production':
    app.config.from_object(config.DefaultConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=KanbanRegisterForm)

from kanban.controllers import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
