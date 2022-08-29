from wtforms import Form, StringField, validators


class KanbanListForm(Form):
    list_name = StringField('Name', [validators.DataRequired(), validators.Length(max=25)])
