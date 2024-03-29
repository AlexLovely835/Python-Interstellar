from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#
#  This file uses the SQL Alchemy DB to define SQL tables.
#

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    privilege_level = db.Column(db.Integer, default=1)
    last_online = db.Column(db.DateTime, default=datetime.utcnow)
    created_storylets = db.relationship('Storylet', backref='author', lazy='dynamic')
    current_hand = db.relationship('Hand', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Storylet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    branches = db.relationship('Branch', backref='parent_storylet', lazy='dynamic')
    deck = db.Column(db.String)
    area = db.Column(db.String)
    urgency = db.Column(db.String)
    order = db.Column(db.Integer)
    notes = db.Column(db.Text)
    escapable = db.Column(db.Boolean)
    tag = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_edit = db.Column(db.DateTime, default=datetime.utcnow())
    last_editor = db.Column(db.String)
    in_hand = db.relationship('Hand', backref='storylet', lazy='dynamic')
    requirements = db.relationship('StoryletQualityRequirements', backref='requirements', lazy='dynamic')

    def __repr__(self):
        return '<Storylet ID{}: {}, By: {}>'.format(self.id, self.title, self.author)

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    button_text = db.Column(db.String)
    storylet_id = db.Column(db.Integer, db.ForeignKey('storylet.id'))
    results = db.relationship('Result', backref='parent_branch', lazy='dynamic')
    notes = db.Column(db.Text)
    order = db.Column(db.Integer)
    action_cost = db.Column(db.Integer)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    next_id = db.Column(db.Integer)
    type = db.Column(db.String)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    random_weight = db.Column(db.Integer)
    area_change = db.Column(db.String)
    notes = db.Column(db.String)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    storylet_id = db.Column(db.Integer, db.ForeignKey('storylet.id'))
    slot = db.Column(db.Integer)

class Quality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    notes = db.Column(db.String)
    display = db.Column(db.String)
    category = db.Column(db.String)
    tag = db.Column(db.String)

class StoryletQualityRequirements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    minimum = db.Column(db.Integer)
    maximum = db.Column(db.Integer)
    quality_id = db.Column(db.Integer, db.ForeignKey('quality.id'))
    storylet_id = db.Column(db.Integer, db.ForeignKey('storylet.id'))