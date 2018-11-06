from stst_project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# friendship = db.Table('friendship', db.Base.meatadata, db.Column )

games = db.Table('games',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True))

# buddies = db.Table('buddies',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable = False)
    password_hashed = db.Column(db.String(128), nullable = False)
    email = db.Column(db.Text, nullable = False)
    xp = db.Column(db.Integer, nullable = False)
    games = db.relationship('Game', secondary='games', lazy='subquery', backref=db.backref('users', lazy=True))
    turns = db.relationship('Turn', backref='user', lazy=True)
    # game_requests =
    # buddies = db.relationship('User',
    # buddy_requests =

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hashed = generate_password_hash(password)
        self.xp = 0

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

    def __repr__(self):
        return "User: " + self.username


class Game(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    turns = db.relationship('Turn', backref='game', lazy=True)

    def __repr__(self):
        return "Game ID: " + str(self.id)

class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, content_input):
        self.content = content_input

    def __repr__(self):
        return "Turn: " + self.content + " at " + str(self.timestamp) + " from " + self.user.username + " in game " + str(self.game)
