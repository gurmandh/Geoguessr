#imports
from . import db, login_manager
from flask import current_app as app
from flask_login import UserMixin

from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    avatar = db.Column(db.String(40), nullable=False, default='default.png')
    account_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'   {self.firstname} {self.lastname} - {self.email}'
    
class ScoreBoard(db.Model):
    __tablename__ = 'scoreboard'
    id = db.Column('id', db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column('score', db.Integer, nullable=False)
    scored_at = db.Column('scored_at', db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User")

# This is for the leaderboard route!!!!
# scores = ScoreBoard.query.order_by(ScoreBoard.score.desc()).limit(10).all()
#snippet code might need some more cuz i checked with trying to run, and there was an issue with "ScoreBoard.c.score.desc()"

class Geolocation(db.Model):
     __tablename__ = 'GeoLocation'
     id = db.Column(db.Integer, primary_key=True)
