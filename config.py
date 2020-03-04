import os
basedir = os.path.abspath(os.path.dirname(__file__))
# import redis
# from os import environ

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SESSION_TYPE = environ.get('SESSION_TYPE')
    # SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))