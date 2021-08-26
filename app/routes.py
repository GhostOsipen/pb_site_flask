from os import abort
from flask import config, render_template, make_response, redirect, url_for, request, abort
from flask.json import jsonify
from flask_login.utils import login_required, logout_user
from werkzeug.security import check_password_hash
from app import app
from app import db
from app.models import User, Note, token_required
import jwt
import datetime


@app.route('/')
@app.route('/index')
def index(): 
    
    return ''

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401,{'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401,{'WWW-Authenticate': 'Basic realm="Login required!"'})

    #if check_password_hash(user.password_hash, auth.password):
    if user.check_password(auth.password):   
        secret='secret'
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret, algorithm="HS256")

        return jsonify({'user': user.username ,'token': token})
        
    return make_response('Could not verify', 401,{'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get('username')    
    password = request.json.get('password')
    email = request.json.get('email')

    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(({ 'username': user.username }))

@app.route('/user', methods=["GET","POST"])
@token_required
def user(current_user):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    notes = user.notes.all()
 
    notesArr = []
    for note in notes:
        notesArr.append(note.toDict()) 
    return jsonify(notesArr)

@app.route('/user/note', methods=["POST"])
@token_required
def add_note(current_user):
    if not request.json or not 'name' in request.json:
        abort(400)

    #user = User.query.filter_by(id=current_user.id).first_or_404()#current_user
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    phone = request.json.get('phone')

    notes = Note(name=name, last_name=last_name, phone=phone, author=current_user)
    db.session.add(notes)
    db.session.commit()

    return jsonify({'name': name})

@app.route('/user/note/<id>', methods=['PUT']) 
@token_required
def edit_note(current_user, id):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    note = Note.query.get(id) #get note by id

    note.name = request.json.get('name')
    note.last_name = request.json.get('last_name')
    note.phone = request.json.get('phone')

    db.session.commit()

    return jsonify({'name': note.name})

@app.route('/user/note/<id>', methods=['DELETE'])
@token_required
def delete_note(current_user, id):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    Note.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/admin/users', methods=["GET", "POST"])
def admin_users():
    users = User.query.all()

    usersArr = []
    for user in users:
        usersArr.append(user.toDict()) 
    return jsonify(usersArr)

@app.route('/admin/notes', methods=["GET", "POST"])
def admin_notes():
    user = User.query.filter_by(username="Max").first_or_404()
    notes = user.notes.all()
 
    notesArr = []
    for note in notes:
        notesArr.append(note.toDict()) 
    return jsonify(notesArr)
