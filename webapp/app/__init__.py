import flask
from flask.ext.httpauth import HTTPBasicAuth

from app import views
from app import models
#from werkzeug.contrib.fixers import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

#Create an Instance of Flask
app = flask.Flask(__name__)
auth = HTTPBasicAuth()

#Include config from config.py
app.config.from_object('config')

