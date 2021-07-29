from os import name
from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required, logout_user
from app import app
from app import db
from app.forms import AddNoteForm, EditNoteForm, LoginForm, RegistrationForm
from app.models import User, Note
from flask_login import current_user, login_user
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index(): 
    books = [
        {   
            'name':{'username':'Max'},
            'phone': "111"
        },
        {
            'name':{'username':'Eugene'},
            'phone': "222"
        }

    ]
    return render_template("index.html", title="Home", books=books)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now a registered user")
        return redirect(url_for("login"))
    return render_template("registration.html", title="Register", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    notes = user.notes.all()
    return render_template('user.html', user=user, notes=notes)

@app.route('/user/add_note', methods=["GET", "POST"])
@login_required
def add_note():
    user = current_user
    form = AddNoteForm()
    if form.validate_on_submit():
        notes = Note(name=form.name.data, last_name=form.last_name.data, phone=form.phone.data, author=user)
        db.session.add(notes)
        db.session.commit()
        flash('Note added')
        return redirect(url_for('user', username=current_user.username))
    return render_template('add.html', title='Add note', user=user, form=form)

@app.route('/user/edit_note/<id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    user = current_user
    form = EditNoteForm()
    note = Note.query.get(id) #get note by id
    if form.validate_on_submit():
        #notes = Note(name=form.name.data, last_name=form.last_name.data, phone=form.phone.data, author=user)
        note.name = form.name.data
        note.last_name = form.last_name.data
        note.phone = form.phone.data
        db.session.commit()
        flash('Note changed')
        return redirect(url_for('user', username=current_user.username))
    return render_template('edit.html', title='Edit note', user=user, form=form, note=note)

@app.route('/User/delete_note/<id>', methods=['POST', 'GET'])
@login_required
def delete_note(id):
    Note.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))

@app.route('/admin', methods=["GET", "POST"])
def admin():
    users = User.query.all()

    return render_template('admin.html', users=users)
