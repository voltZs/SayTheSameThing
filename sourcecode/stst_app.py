#!/usr/bin/python3

from flask import Flask, request, render_template, redirect, abort, flash, session, url_for, jsonify
from stst_project import app, db
from stst_project.models import User, Game, Turn, Notification
from flask_login import current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

db.create_all()


@app.route('/')
def home():
    curr_user_leveling = {}
    new_notifications = {}
    if current_user.is_authenticated:
        curr_user_leveling = user_level_info(current_user)
        new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('home.html', curr_user_leveling=curr_user_leveling, new_notifications=new_notifications)

@app.route('/register')
def register():
    if request.args:
        avatar = request.args.get('avatar')
        username = request.args.get('username')
        password = request.args.get('password')
        password_conf = request.args.get('password_conf')
        email = request.args.get('email')
        session['prev_form'] = {'username' : username, 'email': email, 'avatar': avatar}

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
        user = User(username, email, password, avatar)
        db.session.add(user)
        db.session.commit()
        if session.get('prev_form'):
            session['prev_form'] = None
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
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('welcome.html', curr_user_leveling=curr_user_leveling, new_notifications=new_notifications)

@app.route('/games')
@login_required
def my_games():
    current_games = []
    finished_games = []
    users_games = current_user.games

    if users_games:
        for game in users_games:
            if game.won:
                finished_games.append(create_game_dict(game))
            else:
                current_games.append(create_game_dict(game))

    curr_user_leveling = user_level_info(current_user)
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('mygames.html',current_games=current_games, finished_games=finished_games, curr_user_leveling=curr_user_leveling, new_notifications=new_notifications)

@app.route('/buddies')
@login_required
def my_buddies():
    buddies = current_user.buddies

    curr_user_leveling = user_level_info(current_user)
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('mybuddies.html', curr_user_leveling=curr_user_leveling, new_notifications=new_notifications, buddies=buddies)


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
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('usersearch.html', search_results=search_results, recent_users=recent_users, curr_user_leveling=curr_user_leveling, new_notifications=new_notifications)

@app.route('/user_settings')
@login_required
def user_me():
    user = current_user
    user_leveling = user_level_info(current_user)
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('usersettings.html', user=user, user_leveling=user_leveling, curr_user_leveling=user_leveling, new_notifications=new_notifications)


@app.route('/user/<username>')
@login_required
def user_page(username):
    if username == current_user.username:
        return redirect(url_for('user_me'))
    user = User.query.filter_by(username=username).first()
    if user == None:
        return abort(404, 'This user does not exist or has been deleted.')
    user_leveling = user_level_info(user)
    games = []
    for game in user.games:
        if current_user in game.users:
            games.append(create_game_dict(game))
    curr_user_leveling = user_level_info(current_user)
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('userpage.html', user=user, games=games, user_leveling=user_leveling, curr_user_leveling=curr_user_leveling, new_notifications=new_notifications)

@app.route('/user/<username>/add_buddy')
@login_required
def add_buddy(username):
    new_buddy = User.query.filter_by(username=username).first()
    if new_buddy:
        if not new_buddy in current_user.buddies:
            current_user.buddies.append(new_buddy)
            notification = Notification()
            notification.content = str(current_user.username) + " added you as their buddy."
            notification.link = "/user/" + current_user.username
            new_buddy.notifications.append(notification)
            db.session.add(current_user)
            db.session.add(notification)
            db.session.add(new_buddy)
            db.session.commit()
        else:
            flash("This user is already your buddy")
            return redirect('/user/'+username)
    else:
        return abort(404, "The user you are trying to add as a buddy was not found")
    return redirect(url_for('my_buddies'))

@app.route('/user/<username>/remove_buddy')
@login_required
def remove_buddy(username):
    buddy = User.query.filter_by(username=username).first()
    if buddy:
        if buddy in current_user.buddies:
            current_user.buddies.remove(buddy)
            db.session.add(current_user)
            db.session.commit()
        else:
            flash("This user is not in your buddies")
            return redirect('/user/'+username)
    else:
        return abort(404, "The user you are trying to remove from buddies was not found")
    return redirect(url_for('my_buddies'))

@app.route('/play_random')
@login_required
def play_random():
    current_user.waiting_for_a_game=True
    db.session.add(current_user)
    db.session.commit()
    curr_user_leveling = user_level_info(current_user)
    new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('gamewait.html', curr_user_leveling=curr_user_leveling, new_notifications=new_notifications, )

@app.route('/start_game/<username>')
@login_required
def start_game_with_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        new_game = Game()
        new_game.users.append(user)
        new_game.users.append(current_user)
        db.session.add(new_game)
        db.session.commit()

        notification = Notification()
        notification.link = "/play/" + str(new_game.id)
        notification.content = current_user.username + " started a new game with you."
        user.notifications.append(notification)

        db.session.add(new_game)
        db.session.add(notification)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('play', game_id=new_game.id))
    else:
        return abort(404, 'The user you are trying to play with does not exist.')


@app.route('/play/<game_id>')
@login_required
def play(game_id):
    game = Game.query.get(game_id)
    if game:
        other_user = get_other_user(game)
        if current_user in game.users:
            curr_user_turns = get_turns(game, current_user)
            other_user_turns = get_turns(game, other_user)
            game_status = compare_turns(curr_user_turns, other_user_turns)
            rounds = (max(len(curr_user_turns ), len(other_user_turns)))
            earnable_xp = get_game_xp(rounds)
            if check_game_won(curr_user_turns, other_user_turns):
                # add XP points if not already added
                if not game in current_user.retrieved_from_games:
                    current_user.xp += earnable_xp
                    current_user.retrieved_from_games.append(game)
                    db.session.add(current_user)
                    db.session.commit()
                game_status = 'STATUS_WON'
                game.won = True
                db.session.add(game)
                db.session.commit()
            curr_user_leveling = user_level_info(current_user)
            new_notifications = get_unseen_notific(current_user.notifications)
            other_user_leveling = user_level_info(other_user)

            return render_template('game.html',
                                    game_id=game.id,
                                    other_user=other_user,
                                    other_user_leveling=other_user_leveling,
                                    other_user_turns=other_user_turns,
                                    curr_user_leveling=curr_user_leveling,
                                    new_notifications=new_notifications,
                                    curr_user_turns=curr_user_turns,
                                    earnable_xp=earnable_xp,
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

@app.route('/clear_notifications', methods=["POST"])
def clear_notifications():
    for notification in current_user.notifications:
        notification.viewed=True
        db.session.add(notification)
    db.session.commit()
    return "Notifications cleared"

@app.route('/change_avatar', methods=["POST"])
def change_avatar():
    new_avatar = request.form['avatar']
    current_user.avatar = new_avatar
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('user_me'))

@app.route('/delete_account')
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('home'))

############################ POLLING ############################

@app.route('/poll')
def poll_game():
    passed_in_turns = request.args.get("otherTurns")
    game_id = request.args.get("gameId")
    counter = 0
    while True:
        time.sleep(3)
        counter += 1
        db.session.commit() #need to run this to get real time data from db for some reason
        game = Game.query.get(game_id)
        other_user = get_other_user(game)
        other_user_turns = get_turns(game, other_user)
        numOfTurns = str(len(other_user_turns))
        #if there is a change or a minute has passed return the number
        if not numOfTurns == passed_in_turns or counter > 20:
            return numOfTurns

@app.route('/find_waiting_user')
def poll_waiting_users():
    db.session.commit()
    users = User.query.filter_by(waiting_for_a_game=True)
    counter = 0
    # check if I am still waiting for a game if yes look for others who are too
    while True:
        db.session.commit()
        if current_user.waiting_for_a_game==False:
            my_games = current_user.games
            return str(my_games[len(my_games)-1].id)
        for other_user in users:
            if not other_user == current_user:
                new_game = Game()
                new_game.users.append(current_user)
                new_game.users.append(other_user)
                other_user.waiting_for_a_game=False
                current_user.waiting_for_a_game=False
                db.session.add(other_user)
                db.session.add(current_user)
                db.session.add(new_game)
                db.session.commit()
                return str(new_game.id)
        time.sleep(3)
        counter += 1
        if counter > 22:
            return None

@app.route('/check_notifications')
def poll_notifications():
    passed_in_num = int(request.args.get("numOfNotifications"))
    new_notifications = get_unseen_notific(current_user.notifications)
    return str(len(new_notifications))

@app.route('/get_notifications')
def get_notifications():
    notifications = []
    for notification in current_user.notifications:
        new_notification = create_notific_dict(notification)
        notifications.append(new_notification)
    return jsonify(notifications)

################################# ERRORS ##################################

@app.errorhandler(404)
def page_not_found(error):
    curr_user_leveling = {}
    if current_user.is_authenticated:
        curr_user_leveling = user_level_info(current_user)
        new_notifications = get_unseen_notific(current_user.notifications)
    return render_template('err404.html', error_msg=error, curr_user_leveling=curr_user_leveling, new_notifications=new_notifications), 404


####################   OTHER FUNCTIONS   ############################

def check_username_existing(username_input):
    if User.query.filter_by(username=username_input).first():
        raise Exception("Username already registered.")

def check_email_existing(email_input):
    if User.query.filter_by(email=email_input).first():
        raise Exception("Email already registered.")

def user_level_info(user):
    level_info = {
        "xp_to_level": calculate_xp_to_level(user),
        "prev_mark": get_level_marks()[calculate_level(user.xp)],
        "next_mark": get_level_marks()[calculate_level(user.xp)+1],
        "level" : calculate_level(user.xp)
    }
    return level_info

def get_level_marks():
    return [((150*x*x)) for x in range(0,50)]

def calculate_level(xp):
    level_marks = get_level_marks()
    for mark_index in range(len(level_marks)):
        if xp >= level_marks[mark_index] and xp < level_marks[mark_index+1]:
            return mark_index

def calculate_xp_to_level(user):
    level = calculate_level(user.xp)
    level_marks = get_level_marks()
    previous_mark = level_marks[level]
    next_mark = level_marks[level+1]
    return (user.xp-previous_mark)/(next_mark)

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

def check_game_won(turns1, turns2):
    if len(turns1) == len(turns2):
        last_item1='A'
        last_item2='B'
        if turns1:
            last_item1 = turns1[len(turns1)-1]['content']
        if turns2:
            last_item2 = turns2[len(turns2)-1]['content']
        return last_item1.lower() == last_item2.lower()
    return False

def get_game_xp(rounds):
    if not rounds:
        rounds = 1
    xps = [150, 100, 80, 60, 50, 45, 40, 35, 30, 27, 24, 21, 18, 16, 14, 12, 10]
    if rounds > len(xps):
        return 5
    else:
        return xps[rounds-1]

def create_game_dict(game):
    game_dict = {}
    game_dict['id'] = game.id
    for user in game.users:
        if not user == current_user:
            game_dict['opponent'] = user
    curr_user_turns = get_turns(game, current_user)
    other_user_turns = get_turns(game, game_dict['opponent'])
    rounds = (max(len(curr_user_turns ), len(other_user_turns)))
    game_dict['turns'] = rounds
    game_dict['status'] = compare_turns(curr_user_turns, other_user_turns)
    if game.won:
        game_dict['status'] = 'STATUS_WON'
    return game_dict

def create_notific_dict(notification):
    notif_dict = {}
    notif_dict['content'] = notification.content
    notif_dict['link'] = notification.link
    notif_dict['viewed'] = notification.viewed
    return notif_dict

def get_unseen_notific(notifications):
    new_notifications = []
    for item in notifications:
        if item.viewed == False:
            new_notifications.append(item)
    return new_notifications


if __name__ == '__main__':
    app.run(debug = True, threaded=True)
