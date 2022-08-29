from wtforms import Form, SelectField, StringField, TextAreaField, DateField, BooleanField
from wtforms import validators, ValidationError
from datetime import date


class KanbanCardForm(Form):
    list = SelectField('List', [validators.DataRequired()], coerce=int)

    title = StringField('Title', [validators.DataRequired(), validators.Length(max=25)])

    content = TextAreaField('Content', [validators.Length(max=250)])

    deadline = DateField('Deadline', [validators.DataRequired()])

    completed = BooleanField('Mark as complete')

    def validate_deadline(self, field):
        if not self.completed.data and field.data < date.today():
            raise ValidationError('Deadline must be set to today or a later date if the task is not completed.')
