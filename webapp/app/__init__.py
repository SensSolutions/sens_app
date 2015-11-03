from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# Create an Instance of Flask
from flask import Flask
app = Flask(__name__)

# Include config from config.py
app.config.from_object('config')

from app import views, models

"""
from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth

from werkzeug.contrib.fixers import ProxyFix

#Create an Instance of Flask
app = Flask(__name__)
auth = HTTPBasicAuth()

app.wsgi_app = ProxyFix(app.wsgi_app)
#Include config from config.py
app.config.from_object('config')

from app import views
#from app import views, models
#from app.views import api
"""
