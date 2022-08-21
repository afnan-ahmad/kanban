from flask import Flask

app = Flask(__name__, template_folder='templates')
app.app_context().push()

from kanban.controllers import *
