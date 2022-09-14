from flask import render_template
from flask_security import login_required

from kanban import app


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')
