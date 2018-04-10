import flask
from flask import render_template

from game import app

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.djhtml',
    )


@app.route('/static/<path:filepath>')
def serve_static(filename):
    return flask.url_for('static', filename)