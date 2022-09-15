from flask import render_template
from flask_security import login_required, current_user
from flask_jwt_extended import create_access_token

from kanban import app


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/api_access', methods=['GET'])
@login_required
def api_access():
    token = create_access_token(identity=current_user.id)
    return render_template('dialogs/api_access_dialog.html', token=token)
