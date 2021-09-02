from flask import json, request
from flask.json import jsonify
from app import app
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from sqlalchemy import inspect
from functools import wraps

import app

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    
    def toDict(self): #for jsonify
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

#hash password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
#check hash password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.username}"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    last_name = db.Column(db.String(140))
    phone = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def toDict(self): #for jsonify
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
    def __repr__(self):
        return f"Note {self.name}"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        secret='secret'

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:# decoding the payload to fetch the stored details
            token_data = jwt.decode(token, secret, algorithms="HS256")
            current_user = User.query.filter_by(id=token_data['id']).first()
        except:
            return jsonify({'message': 'Token invalid', 'token': token}), 401

        return f(current_user, *args, **kwargs)
    return decorated 
