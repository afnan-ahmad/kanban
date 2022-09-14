import os

from flask_security import Security, SQLAlchemyUserDatastore

from kanban import app, config
from kanban.database import db
from kanban.models import User, Role
from kanban.forms import KanbanRegisterForm

import kanban.util as util


@app.context_processor
def utility_functions():
    return dict(util=util)


if os.getenv('ENV', 'development') == 'production':
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=KanbanRegisterForm)

from kanban.controllers import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)