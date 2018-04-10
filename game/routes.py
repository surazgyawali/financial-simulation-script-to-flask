from flask import render_template

from game import app

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.djhtml',
        title = "HOME",
        desc = "This is the begining."
    )