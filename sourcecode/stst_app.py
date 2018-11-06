from flask import Flask, request, render_template, redirect, abort, flash, session, url_for
from stst_project import app, db
from stst_project.models import User
from flask_login import login_user, login_required, logout_user
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
        password_conf = request.args.get('password_conf')
        email = request.args.get('email')
        session['prev_form'] = {'username' : username, 'email': email}

        # make sure all necessary args are not none
        if username == None or password == None or email == None:
            return redirect('/register')

        if not password == password_conf:
            flash('Your passwords were not matching')
            return redirect('/register')
        try:
            check_username_existing(username)
            check_email_existing(email)
        except Exception as msg:
            flash(msg.args[0])
            return redirect('/register')
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    if not session.get('prev_form'):
        session['prev_form'] = {}
    return render_template('register.html', prev_form = session['prev_form'])

@app.route('/login')
def login():
    if request.args.get('username') and request.args.get('password'):
        username = request.args.get('username')
        password = request.args.get('password')

        # only login if username and password are not None
        if not username == None and not password == None:
            user = User.query.filter_by(username=username).first()
            if user.check_password(password) and not user == None:
                login_user(user)

        return redirect(url_for('welcome'))
    return render_template('login.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user_settings')
@login_required
def user_me():
    return render_template('usersettings.html')

@app.route('/games')
@login_required
def my_games():
    return render_template('mygames.html')

@app.route('/buddies')
@login_required
def my_buddies():
    return render_template('mybuddies.html')

@app.route('/users')
@login_required
def user_search():
    return render_template('usersearch.html')

@app.route('/user/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        return abort(404, 'This user does not exist or has been deleted.')
    return render_template('userpage.html', user=user)

# @app.route('/play_random') <redirect to game but fetch a random player
# @login_required
#
# @app.route('/play')
# @login_required

@app.errorhandler(404)
def page_not_found(error):
    return render_template('err404.html', error_msg=error)


def check_username_existing(username_input):
    if User.query.filter_by(username=username_input).first():
        raise Exception("Username already registered.")

def check_email_existing(email_input):
    if User.query.filter_by(email=email_input).first():
        raise Exception("Email already registered.")

if __name__ == '__main__':
    app.run(debug = True)
