import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123123@localhost/user_information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
