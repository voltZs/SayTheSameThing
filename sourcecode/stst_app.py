from flask import Flask, request, render_template, redirect, abort, flash, session, url_for, jsonify
from stst_project import app, db
from stst_project.models import User, Game, Turn
from flask_login import current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

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
    curr_user_leveling = user_level_info(current_user)
    return render_template('welcome.html', curr_user_leveling=curr_user_leveling)

@app.route('/user_settings')
@login_required
def user_me():
    curr_user_leveling = user_level_info(current_user)
    return render_template('usersettings.html', curr_user_leveling=curr_user_leveling)

@app.route('/games')
@login_required
def my_games():
    current_games = []
    finished_games = []
    users_games = current_user.games

    if users_games:
        for game in users_games:
            if game.won:
                finished_games.append(game)
            else:
                current_games.append(game)

    curr_user_leveling = user_level_info(current_user)
    return render_template('mygames.html',current_games=current_games, finished_games=finished_games, curr_user_leveling=curr_user_leveling)

@app.route('/buddies')
@login_required
def my_buddies():
    curr_user_leveling = user_level_info(current_user)
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

    curr_user_leveling = user_level_info(current_user)
    return render_template('usersearch.html', search_results=search_results, recent_users=recent_users, curr_user_leveling=curr_user_leveling)


@app.route('/user/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        return abort(404, 'This user does not exist or has been deleted.')
    curr_user_leveling = user_level_info(current_user)
    return render_template('userpage.html', user=user, curr_user_leveling=curr_user_leveling)

# @app.route('/play_random') <redirect to game but fetch a random player
# @login_required
#

@app.route('/play/<game_id>')
@login_required
def play(game_id):
    game = Game.query.get(game_id)
    if game:
        other_user = get_other_user(game)
        if current_user in game.users:
            curr_user_leveling = user_level_info(current_user)
            curr_user_turns = get_turns(game, current_user)
            other_user_leveling = user_level_info(other_user)
            other_user_turns = get_turns(game, other_user)
            game_status = compare_turns(curr_user_turns, other_user_turns)
            if check_game_won(game, curr_user_turns, other_user_turns):
                game_status = 'STATUS_WON'
                game.won = True
                db.session.add(game)
                db.session.commit()
            rounds = (max(len(curr_user_turns ), len(other_user_turns)))
            return render_template('game.html',
                                    game_id=game.id,
                                    other_user=other_user,
                                    other_user_leveling=other_user_leveling,
                                    other_user_turns=other_user_turns,
                                    curr_user_leveling=curr_user_leveling,
                                    curr_user_turns=curr_user_turns,
                                    game_status=game_status,
                                    rounds=rounds)
        else:
            return abort(404, 'You do not have access to this game.'), 404
    else:
        return abort(404, 'This game does not exist or has been deleted'), 404

@app.route('/submit_answer')
@login_required
def create_turn():
    game = Game.query.get(request.args.get('game_id'))
    user = User.query.get(request.args.get('user_id'))
    game_status = request.args.get('game_status')
    answer = request.args.get('answer')
    turn = Turn(answer)

    if game_status == 'STATUS_GO':
        if game and user:
            if user == current_user:
                game.turns.append(turn)
                user.turns.append(turn)
                db.session.add(game)
                db.session.add(user)
                db.session.commit()
                # REDIRECT MIGHT GET ELIMINATED AFTER MAKING THIS ASYNCHRONOUS
                return redirect(url_for('play', game_id=game.id))
            else:
                return abort(404, 'You can only submit your own turns'), 404
        else:
            return abort(404, 'Game ID or User ID not found.'), 404
    elif game_status == 'STATUS_WON':
        return abort(404, "This game is finished"), 404
    else:
        return abort(404, "You cannot submit an answer when it's the opponent's turn"), 404

############################ POLLING ############################

# @app.route('/poll')
# def poll():
#     passed_in_turns = request.args.get("otherTurns")
#     game_id = request.args.get("gameId")
#
#     while True:
#         time.sleep(2)
#         game = Game.query.get(game_id)
#         other_user = get_other_user(game)
#         other_user_turns = get_turns(game, other_user)
#         numOfTurns = str(len(other_user_turns))
#         print(numOfTurns)
#         print(passed_in_turns)
#         print(other_user.username)
#         print(current_user.username + " " + str(numOfTurns == passed_in_turns))
#
#         if not numOfTurns == passed_in_turns:
#             return numOfTurns

@app.route('/poll_other_user_moves')
def poll():
    passed_in_turns = request.args.get("otherTurns")
    game_id = request.args.get("gameId")
    game = Game.query.get(game_id)
    other_user = get_other_user(game)
    other_user_turns = get_turns(game, other_user)
    numOfTurns = str(len(other_user_turns))
    return numOfTurns

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
        curr_user_leveling = user_level_info(current_user)
    return render_template('err404.html', error_msg=error, curr_user_leveling=curr_user_leveling), 404


####################   OTHER FUNCTIONS   ############################

def check_username_existing(username_input):
    if User.query.filter_by(username=username_input).first():
        raise Exception("Username already registered.")

def check_email_existing(email_input):
    if User.query.filter_by(email=email_input).first():
        raise Exception("Email already registered.")

def user_level_info(user):
    level_info = {
        "xp_to_level": calculate_xp_to_level(user.xp),
        "level" : calculate_level(user.xp)
    }
    return level_info

def calculate_level(xp):
    return int(xp/20)

def calculate_xp_to_level(xp):
    return float(400/700)

def get_other_user(game):
    other_user ={}
    for user in game.users:
        if not user == current_user:
            other_user = User.query.get(user.id)
    return other_user

def get_turns(game, user):
    ordered_turns = get_ordered_turns(game.turns)
    turns= []
    for turn in ordered_turns:
        if turn in user.turns:
            turn_obj = {
                "content" : turn.content,
                "timestamp" : verbose_timestamp(turn.timestamp)
            }
            turns.append(turn_obj)
    return turns

def get_ordered_turns(turns):
    tuples = []
    for turn in turns:
        tuples.append((turn, turn.timestamp))
    tuples.sort(key=lambda x: x[1])
    ordered_turns = []
    for tuple in tuples:
        ordered_turns.append(tuple[0])
    return ordered_turns

def verbose_timestamp(timestamp):
    verbose = ""
    passed = datetime.utcnow() - timestamp
    if passed.days>1:
        verbose = str(int(passed.days)) + " days ago"
    elif passed.days == 1:
        verbose = "1 day ago"
    elif passed.seconds >= 2*60*60:
        verbose = str(int(passed.seconds/60/60)) + " hours ago"
    elif passed.seconds < 2*60*60 and passed.seconds >= 60*60:
        verbose = "1 hour ago"
    elif passed.seconds >= 2*60:
        verbose = str(int(passed.seconds/60)) + " minutes ago"
    elif passed.seconds < 2*60 and passed.seconds >= 60:
        verbose = "1 minute ago"
    else:
        verbose = str(int(passed.seconds)) + " seconds ago"
    return verbose

def compare_turns(current_user_turns, other_user_turns):
    if len(other_user_turns) >= len(current_user_turns):
        return 'STATUS_GO'
    elif len(other_user_turns) < len(current_user_turns):
        return 'STATUS_WAIT'

def check_game_won(game, turns1, turns2):
    if len(turns1) == len(turns2):
        last_item1='A'
        last_item2='B'
        if turns1:
            last_item1 = turns1[len(turns1)-1]['content']
        if turns2:
            last_item2 = turns2[len(turns2)-1]['content']
        return last_item1.casefold() == last_item2.casefold()
    return False

if __name__ == '__main__':
    app.run(debug = True, threaded=True)
