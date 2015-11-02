import flask
from flask.ext.httpauth import HTTPBasicAuth

#app = flask.Flask(__name__)
#auth = HTTPBasicAuth()

#from werkzeug.contrib.fixers import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)


@auth.get_password
def get_password(username):
    if username == 'marck':
        return 'sens'
    return None

@auth.error_handler
def unauthorized():
    return flask.make_response(flask.jsonify({'error': 'Unauthorized access'}), 401)


@app.route("/")
@auth.login_required
def index():
    return "Hello, " + flask.request.remote_addr


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return flask.jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        iflask.abort(404)
    return flask.jsonify({'task': task[0]})


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

