from kanban import app
from flask import request, flash, redirect, render_template

loggedIn = False


@app.route('/', methods=['GET'])
def index():
    if loggedIn:
        return render_template('index.html', title='Home', greeting='Good morning, Afnan')

    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    global loggedIn

    loggedIn = username == 'afnan' and password == 'password'

    if not loggedIn:
        flash("Invalid username or password.")

    return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    global loggedIn

    loggedIn = False
    return redirect('/')
