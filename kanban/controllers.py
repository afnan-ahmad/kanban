from flask import redirect, request, render_template
from flask_security import login_required, current_user

from kanban import app
from kanban.models import *
from kanban.database import db
from kanban.forms import KanbanListForm, KanbanCardForm


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/list/create', methods=['GET', 'POST'])
@login_required
def create_list():
    form = KanbanListForm(request.form)

    if request.method == 'POST' and form.validate():
        existing = List.query.with_parent(current_user).filter_by(name=form.list_name.data).first()

        if not existing:
            new_list = List()
            new_list.name = form.list_name.data

            current_user.lists.append(new_list)
            db.session.commit()

            return redirect(f'/#{new_list.id}')
        else:
            form.list_name.errors.append('A list with this name already exists.')

    return render_template('create_update_form.html', form=form,
                           form_title='Create list',
                           button_text='Create')


@app.route('/card/create', methods=['GET', 'POST'])
@login_required
def create_card():
    form = KanbanCardForm(request.form, list=request.args.get('list'))

    form.list.choices = [(lst.id, lst.name) for lst in current_user.lists]

    if request.method == 'POST' and form.validate():
        new_card = Card()
        new_card.list_id = form.list.data
        new_card.title = form.title.data
        new_card.content = form.content.data
        new_card.deadline = form.deadline.data
        new_card.completed = form.completed.data

        db.session.add(new_card)
        db.session.commit()

        return redirect('/')

    return render_template('create_update_form.html', form=form,
                           form_title='Create card',
                           button_text='Create')
