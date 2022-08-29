from flask_security import RegisterForm
from wtforms import StringField, validators


class KanbanRegisterForm(RegisterForm):
    name = StringField('Name', [validators.DataRequired('Name is required')])
