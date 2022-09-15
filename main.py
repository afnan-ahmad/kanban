import os

from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt_extended import JWTManager
from flask_restful import Api

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

jwt = JWTManager(app)
api = Api(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=KanbanRegisterForm)

from kanban.api import ListAPI, CardAPI, SummaryAPI

api.add_resource(ListAPI, '/api/list/', '/api/list/<int:list_id>/')
api.add_resource(CardAPI, '/api/card/', '/api/card/<int:card_id>/')
api.add_resource(SummaryAPI, '/api/summary/', '/api/summary/<int:list_id>/')

from kanban.controllers import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
