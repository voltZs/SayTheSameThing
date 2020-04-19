from stst_project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# friendship = db.Table('friendship', db.Base.meatadata, db.Column )

games = db.Table('games',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True))

point_retrieval = db.Table('point_retrieval',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True))

waiting_list = db.Table()

buddies = db.Table('buddies',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('buddy_id', db.Integer, db.ForeignKey('user.id'))
)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable = False)
    password_hashed = db.Column(db.String(128), nullable = False)
    email = db.Column(db.Text, nullable = False)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    xp = db.Column(db.Integer, nullable = False)
    avatar = db.Column(db.Integer, nullable = False, default=0)
    games = db.relationship('Game', secondary='games', lazy='subquery', backref=db.backref('users', lazy=True))
    turns = db.relationship('Turn', backref='user', lazy=True)
    retrieved_from_games = db.relationship('Game', secondary='point_retrieval', lazy='subquery', backref=db.backref('point_retrievers', lazy=True))
    waiting_for_a_game = db.Column(db.Boolean, nullable=False, default=False)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    buddies = db.relationship('User', secondary= buddies,
        primaryjoin = (buddies.c.user_id == id),
        secondaryjoin = (buddies.c.buddy_id == id),
        lazy=True)
    # game_requests =
    # buddies = db.relationship('User',
    # buddy_requests =

    def __init__(self, username, email, password, avatar):
        self.username = username
        self.email = email
        self.password_hashed = generate_password_hash(password)
        self.avatar = avatar
        self.xp = 0

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

    def change_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def __repr__(self):
        return "User: " + self.username

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # game = db.relationship('Game', backref='notification', uselist=False, lazy=True)
    content = db.Column(db.String, nullable=False)
    link = db.Column(db.String)

    def __repr__(self):
        return "Notification for game " + str(self.game.id) + " sent to user: " + str(self.user.username)


class Game(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    won = db.Column(db.Boolean, nullable=False, default=False)
    turns = db.relationship('Turn', backref='game', lazy=True)
    # notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'))

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
