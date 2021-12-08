import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import config


# declare constants
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
FLASK_TEMPLATE_PATH = BASEDIR + '/templates'
FLASK_STATIC_PATH = BASEDIR + '/static'
SQLITE_PATH = BASEDIR + '/data'

if not os.path.isdir(SQLITE_PATH):
    os.mkdir(SQLITE_PATH)

# initialize Flask and related objects
app = Flask(__name__, template_folder=FLASK_TEMPLATE_PATH, static_folder=FLASK_STATIC_PATH)

# import config from config.py
app.config.from_object(config)

# set SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_PATH + '/data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
