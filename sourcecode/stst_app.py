from flask import Flask, request, render_template, redirect, abort, flash, session
from stst_project import app, db
from stst_project.models import User

from flask_sqlalchemy import SQLAlchemy

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    if request.args:
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        try:
            check_username_existing(username)
            check_email_existing(email)
        except Exception as msg:
            session['prev_form'] = {'username' : username, 'email': email}
            print(session['prev_form'])
            flash(msg.args[0])
            return redirect('/register')
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', prev_form = session['prev_form'])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


def check_username_existing(username_input):
    if User.query.get(username_input):
        raise Exception("Username already registered.")

def check_email_existing(email_input):
    if User.query.filter_by(email=email_input).first():
        raise Exception("Email already registered.")

if __name__ == '__main__':
    app.run(debug = True)
