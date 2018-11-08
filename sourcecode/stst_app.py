from flask import Flask, request, render_template, redirect, abort, flash, session, url_for, jsonify
from stst_project import app, db
from stst_project.models import User
from flask_login import current_user, login_user, login_required, logout_user
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
            if not user == None:
                if user.check_password(password):
                    login_user(user)
                else:
                    flash('The password you entered was incorrect')
                    return redirect(url_for('login'))
            else:
                flash('This username does not exist')
                return redirect(url_for('login'))

        return redirect(url_for('welcome'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/welcome')
@login_required
def welcome():
    curr_user_leveling = curr_user_level_info()
    return render_template('welcome.html', curr_user_leveling=curr_user_leveling)

@app.route('/user_settings')
@login_required
def user_me():
    curr_user_leveling = curr_user_level_info()
    return render_template('usersettings.html', curr_user_leveling=curr_user_leveling)

@app.route('/games')
@login_required
def my_games():
    users_games = current_user.games
    current_games = []
    finished_games = []
    for game in users_games:
        if game.won:
            finished_games.append(game)
        else:
            current_games.append(game)
    curr_user_leveling = curr_user_level_info()
    return render_template('mygames.html',current_games=current_games, finished_games=finished_games, curr_user_leveling=curr_user_leveling)

@app.route('/buddies')
@login_required
def my_buddies():
    curr_user_leveling = curr_user_level_info()
    return render_template('mybuddies.html', curr_user_leveling=curr_user_leveling)


@app.route('/users')
@login_required
def user_search():
    search_results = []
    if request.args:
        results_by_name = User.query.filter_by(username=request.args.get('searchWord'))
        results_by_email = User.query.filter_by(username=request.args.get('searchWord'))

        search_results = results_by_name
        for e_result in results_by_email:
            if not e_result in search_results:
                results.append(e-result)
    recent_users = User.query.all()
    tuples = []
    for user in recent_users:
        tuples.append((user, user.joined))
    tuples.sort(key=lambda x: x[1], reverse=True)
    recent_users = []
    for tuple in tuples:
        if len(recent_users)<10:
            recent_users.append(tuple[0])

    curr_user_leveling = curr_user_level_info()
    return render_template('usersearch.html', search_results=search_results, recent_users=recent_users, curr_user_leveling=curr_user_leveling)


@app.route('/user/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        return abort(404, 'This user does not exist or has been deleted.')
    return render_template('userpage.html', user=user, curr_user_leveling=curr_user_leveling)

# @app.route('/play_random') <redirect to game but fetch a random player
# @login_required
#
# @app.route('/play')
# @login_required



###################### DATA RETRIEVING VIEWS ##################################

@app.route('/current_user_details')
def current_user_details():
    user_details = {
        "username" : current_user.username,
        "xp": current_user.xp,
        "xp_to_level": calculate_xp_to_level(current_user.xp),
        "level" : calculate_level(current_user.xp),
        "email" : current_user.email,
    }
    return jsonify(user_details)

################################# ERRORS ##################################

@app.errorhandler(404)
def page_not_found(error):
    curr_user_leveling = {}
    if current_user.is_authenticated:
        curr_user_leveling = curr_user_level_info()
    return render_template('err404.html', error_msg=error, curr_user_leveling=curr_user_leveling), 404


def check_username_existing(username_input):
    if User.query.filter_by(username=username_input).first():
        raise Exception("Username already registered.")

def check_email_existing(email_input):
    if User.query.filter_by(email=email_input).first():
        raise Exception("Email already registered.")

def curr_user_level_info():
    level_info = {
        "xp_to_level": calculate_xp_to_level(current_user.xp),
        "level" : calculate_level(current_user.xp)
    }
    return level_info

def calculate_level(xp):
    return int(xp/20)

def calculate_xp_to_level(xp):
    return float(400/700)

if __name__ == '__main__':
    app.run(debug = True)
