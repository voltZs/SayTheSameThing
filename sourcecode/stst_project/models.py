from stst_project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# class Game(db.Model):
#     __tablename__ = 'games'
#
#     id= db.Column(db.Integer, primary_key=True)
#     user1 =
#     user2 =
#
#     def __init__(self, user1, user2):
#         self.user1 = user1
#         self.user2 = user2
#
#     def __repr__(self):
#         return "Game ID: " + self.id + ", users: " + self.user1.username + " & " + self.user2.username

# friendship = db.Table('friendship', db.Base.meatadata, db.Column )

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password_hashed = db.Column(db.String(128))
    email = db.Column(db.Text)
    xp = db.Column(db.Integer)
    # games = db.relationship('Game', backref='user', lazy='dynamic')
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
