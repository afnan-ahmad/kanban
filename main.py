import os

from flask import render_template
from flask_security import Security, SQLAlchemyUserDatastore
from flask_restful import Api
from flask_cors import CORS

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

api = Api(app)
cors = CORS(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=KanbanRegisterForm)

from kanban.api import UserAPI, ListAPI, CardAPI, SummaryAPI

api.add_resource(UserAPI, '/api/user')
api.add_resource(ListAPI, '/api/list', '/api/list/<int:list_id>')
api.add_resource(CardAPI, '/api/card', '/api/card/<int:card_id>')
api.add_resource(SummaryAPI, '/api/summary', '/api/summary/<int:list_id>')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
