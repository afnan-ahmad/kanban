from kanban import app
from flask import request, flash, redirect, render_template
from flask_security import login_required, current_user
from kanban.util import greeting_text
from kanban.models import *


@app.route('/', methods=['GET'])
@login_required
def index():
    greeting = greeting_text(current_user.name)
    lists = List.query.filter(List.user_id == current_user.id).all()
    return render_template('index.html', title='Home', greeting=greeting, lists=lists)
