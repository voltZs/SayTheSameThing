from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# DATABASE SETUP
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# LOGIN config
login_manager = LoginManager()

app.config['SECRET_KEY'] = "Saying the same thing gives one pleasure"
login_manager.init_app(app)
login_manager.login_view = 'login'
