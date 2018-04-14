from flask import Flask

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

from game import routes

@app.route('/static/<path:filepath>')
def serve_static(filename):
    return flask.url_for('static', filename)