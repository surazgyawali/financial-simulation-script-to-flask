from flask import Flask

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

from game import routes