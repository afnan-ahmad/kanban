from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired


class KanbanRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])
