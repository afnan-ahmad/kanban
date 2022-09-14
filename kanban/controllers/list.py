from flask import render_template, request, redirect
from flask_security import login_required, current_user

from kanban import app
from kanban.database import db
from kanban.forms import KanbanListForm
from kanban.models import List


def exists_by_name(name):
    return List.query.with_parent(current_user).filter_by(name=name).first() is not None


@app.route('/list/create', methods=['GET', 'POST'])
@login_required
def create_list():
    form = KanbanListForm(request.form)

    if request.method == 'POST' and form.validate():

        if not exists_by_name(form.name.data):
            new_list = List(name=form.name.data)

            current_user.lists.append(new_list)
            db.session.commit()

            return redirect(f'/#{new_list.id}')

        else:
            form.name.errors.append('A list with this name already exists.')

    return render_template('dialogs/create_update_dialog.html', form=form,
                           form_title='Create list',
                           primary_button_text='Create')


@app.route('/list/edit', methods=['GET', 'POST'])
@login_required
def edit_list():
    list_id = request.args.get('id')

    existing_list = List.query.with_parent(current_user).filter_by(id=list_id).first()

    if not existing_list:
        return redirect('/')

    form = KanbanListForm(request.form, name=existing_list.name)

    if request.method == 'POST' and form.validate():

        if form.name.data == existing_list.name:
            return redirect(f'/#{existing_list.id}')

        elif not exists_by_name(form.name.data):
            existing_list.name = form.name.data
            db.session.commit()

            return redirect(f'/#{existing_list.id}')

        else:
            form.name.errors.append('A list with this name already exists.')

    return render_template('dialogs/create_update_dialog.html', form=form,
                           form_title='Edit list',
                           primary_button_text='Save')


@app.route('/list/delete', methods=['POST'])
@login_required
def delete_list():
    list_id = request.form.get('id')

    existing_list = List.query.with_parent(current_user).filter_by(id=list_id).first()

    if not existing_list:
        return redirect('/')

    if len(existing_list.cards) == 0:
        db.session.delete(existing_list)
        db.session.commit()

        return redirect('/')

    move_to = request.form.get('move_to')

    if not move_to:
        return render_template('dialogs/list_delete_dialog.html', list=existing_list)

    elif int(move_to) == -1:
        for card in existing_list.cards:
            db.session.delete(card)

    else:
        move_to_list = List.query.with_parent(current_user).filter_by(id=move_to).first()

        if not move_to_list:
            return redirect('/')

        for card in existing_list.cards:
            card.list_id = move_to_list.id
        db.session.commit()

    db.session.delete(existing_list)
    db.session.commit()

    return redirect('/')
