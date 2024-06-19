from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    iduser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=True)
    useremail = db.Column(db.String(45), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

class Friend(db.Model):
    idfriend = db.Column(db.Integer, primary_key=True, autoincrement=True)
    friendid = db.Column(db.Integer, nullable=False)

    def __init__(self, idfriend, friendid):
        self.idfriend = idfriend
        self.friendid = friendid

    def __repr__(self):
        return f'<Friend(user_id={self.user_id}, friend_id={self.friend_id})>'


class Post(db.Model):
    __tablename__ = 'Post'
    idpost = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, ForeignKey('user.iduser'), primary_key=True, nullable=False)
    content = db.Column(db.String(255), nullable=False)
    postime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, content, userid):
        self.content = content
        self.userid = userid
        self.postime = datetime.utcnow()

