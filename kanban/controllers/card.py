from flask import render_template, request, redirect
from flask_security import login_required, current_user

from kanban import app
from kanban.database import db
from kanban.forms import KanbanCardForm
from kanban.models import Card, List


@app.route('/card/create', methods=['GET', 'POST'])
@login_required
def create_card():
    form = KanbanCardForm(request.form, list=request.args.get('list'))

    form.list.choices = [(lst.id, lst.name) for lst in current_user.lists]

    if request.method == 'POST' and form.validate():

        user_list = List.query.with_parent(current_user).filter_by(id=form.list.data).first()

        if not user_list:
            return redirect('/')

        new_card = Card()
        new_card.title = form.title.data
        new_card.content = form.content.data
        new_card.deadline = form.deadline.data
        new_card.completed = form.completed.data

        new_card.user_id = user_list.user_id

        user_list.cards.append(new_card)

        db.session.commit()

        return redirect(f'/#{new_card.list_id}')

    return render_template('dialogs/create_update_dialog.html', form=form,
                           form_title='Create card',
                           primary_button_text='Create')


@app.route('/card/edit', methods=['GET', 'POST'])
@login_required
def edit_card():
    card_id = request.args.get('id')

    card = Card.query.filter_by(user_id=current_user.id).filter_by(id=card_id).first()

    if not card:
        return redirect('/')

    form = KanbanCardForm(request.form)

    form.list.choices = [(lst.id, lst.name) for lst in current_user.lists]

    if request.method == 'POST' and form.validate():

        user_list = List.query.with_parent(current_user).filter_by(id=form.list.data).first()

        if not user_list:
            return redirect('/')

        card.list_id = user_list.id
        card.title = form.title.data
        card.content = form.content.data
        card.deadline = form.deadline.data
        card.completed = form.completed.data

        db.session.commit()

        return redirect(f'/#{card.list_id}')

    if request.method == 'GET':
        form.list.data = card.list_id
        form.title.data = card.title
        form.content.data = card.content
        form.deadline.data = card.deadline
        form.completed.data = card.completed

    return render_template('dialogs/create_update_dialog.html', form=form,
                           form_title='Edit card',
                           primary_button_text='Save')


@app.route('/card/move', methods=['GET', 'POST'])
@login_required
def move_card():
    card_id = request.args.get('id')

    card = Card.query.filter_by(user_id=current_user.id).filter_by(id=card_id).first()

    if not card:
        return redirect('/')

    if request.method == 'POST':
        move_to = request.form.get('move_to')

        user_list = List.query.with_parent(current_user).filter_by(id=move_to).first()

        if not move_to or not user_list:
            return redirect('/')

        card.list_id = user_list.id

        db.session.commit()

        return redirect(f'/#{card.list_id}')

    return render_template('dialogs/card_move_dialog.html', card=card)


@app.route('/card/toggle_status', methods=['POST'])
@login_required
def toggle_card_status():
    card_id = request.form.get('id')

    card = Card.query.filter_by(user_id=current_user.id).filter_by(id=card_id).first()

    if not card:
        return redirect('/')

    card.completed = not card.completed

    db.session.commit()

    return redirect(f'/#{card.list_id}')


@app.route('/card/delete', methods=['POST'])
@login_required
def delete_card():
    card_id = request.form.get('id')

    card = Card.query.filter_by(user_id=current_user.id).filter_by(id=card_id).first()

    if not card:
        return redirect('/')

    list_id = card.list_id

    db.session.delete(card)
    db.session.commit()

    return redirect(f'/#{list_id}')
