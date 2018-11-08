from stst_project import app, db
from stst_project.models import User, Game, Turn
from flask_sqlalchemy import SQLAlchemy

db.create_all()
#
# user1 = User('tralala', 'tralala@trala.la', 'password123')
# user2 = User('kokoto', 'kokoto@koko.to', 'password321')
# db.session.add(user1)
# db.session.add(user2)
# db.session.commit()
#
# retrieved_user1 = User.query.filter_by(username='matt.d').first()
# retrieved_user2 = User.query.filter_by(username='honey.bunny').first()
# game = Game()
# game.users.append(retrieved_user1)
# game.users.append(retrieved_user2)
# db.session.add(game)
# db.session.commit()
#
# retrieved_user1 = User.query.filter_by(username='tralala').first()
# turn1 = Turn('Bed')
# retrieved_user1.turns.append(turn1)
#
# retrieved_user2 = User.query.filter_by(username='kokoto').first()
# turn2 = Turn('Sofa')
# retrieved_user2.turns.append(turn2)
#
# game = Game.query.get(1)
# game.turns.append(turn1)
# game.turns.append(turn2)
#
# db.session.add(game)
# db.session.add_all([retrieved_user1,retrieved_user2])
# db.session.commit()

# tralala = User.query.filter_by(username='tralala').first()
# kokoto = User.query.filter_by(username='kokoto').first()
#
# kokoto.buddies.append(tralala)
# db.session.add(kokoto)
# db.session.commit()
#
# print(User.query.filter_by(username='tralala').first().buddies)
# print(User.query.filter_by(username='kokoto').first().buddies)

# User.query.filter_by(username='tralala').first().buddies.append(kokoto)
# db.session.add(tralala)
# db.session.commit


# print(User.query.filter_by(username='tralala').first().turns[0])
# print(User.query.filter_by(username='kokoto').first().turns[0])
# print(Game.query.get(1).turns)



# users = User.query.all()
# games = Game.query.all()
#
# print(users)
# print(games[0].users)
