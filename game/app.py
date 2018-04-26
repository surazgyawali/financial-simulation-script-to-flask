import logging

import flask
from flask_cors import CORS
from flask_restful import Api
from game.resources import GameResource
app = flask.Flask(__name__)
api = Api(app)
cors = CORS(app)
from game import routes
from game import config

app.config.from_object(config)
app.secret_key = 'my unobvious secret key'
api.add_resource(GameResource, '/api/game')


app.in_queue = {}
app.out_queue = {}