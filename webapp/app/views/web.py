from app import app
import flask
from flask.ext.httpauth import HTTPBasicAuth


@app.route("/")
@app.route('/index')
# @auth.login_required
def index():
    return "Hello, " + flask.request.remote_addr
