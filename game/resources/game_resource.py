from flask_restful import Resource, reqparse
from flask import current_app as app
from game.services import GameService
from threading import Lock
import logging
from pickle import loads
from uuid import uuid4
import time

class GameResource(Resource):
    def __init__(self):
        self.in_queue = app.in_queue
        self.out_queue = app.out_queue
        self.queue_key = app.config['QUEUE_KEY']
        self.lock = Lock()

    def __set_value(self, sessid, message):
        key = '{}:{}'.format(self.queue_key, sessid)
        value = message
        self.lock.acquire()
        self.in_queue[sessid][key] = value
        self.lock.release()

    def __get_value(self, sessid):
        '''Retrives an entry from the queue '''
        if not self.out_queue.get(sessid, None):
            return -1, None
        key = '{}:{}'.format(self.queue_key, sessid)
        retry_count = 5
        for _ in range(retry_count):
            start = time.time()
            value = self.out_queue[sessid].get(key, None)
            end = time.time()
            if value is not None:
                status = 0
                break
            else:
                time.sleep(1)
                continue
        if value is None:
            status = -1
        else:
            self.out_queue[sessid] = {}

        return status, value

    def get(self):
        '''Subsequent get requests from client side with sessid and response message returns the game state'''
        parser = reqparse.RequestParser(bundle_errors = True)
        parser.add_argument('sessid', required = False, type = str, default = 'default', location = 'headers', help = 'Id of the session.')
        parser.add_argument('message', required = False, type = str, default = '', location = 'headers', help = 'Selection response from client.')

        args = parser.parse_args()
        sessid = args.sessid
        message = args.message
        self.__set_value(sessid, message)
        start_time = time.time()
        status = -1
        while status == -1:
            status, result = self.__get_value(sessid)
        end_time = time.time()

        if status != 0:
            result = dict({'Error' : 'Entry not found!'})

        response =  dict({'status' : status, 'data' : result, 'sessid' : sessid})
        return response

    def post(self):
        '''Initial post request from client side starts a new game'''
        parser = reqparse.RequestParser(bundle_errors = True)
        parser.add_argument('sessid', required = False, type = str, location = 'headers', help = 'Id of the session.')

        args = parser.parse_args()
        sessid = args.sessid

        if not sessid:
            sessid = str(uuid4())
        game_service = GameService(sessid)
        status, result = game_service.init_game()
        game_service.start()
        result = None
        if status == 0:
            status = -1
            while status == -1:
                status, result = self.__get_value(sessid)
            print (result)
        if status == 0:
            result = dict({'status' : status, 'data': result,  'sessid' : sessid})
        else:
            result = dict({'status' : status, 'error' : 'Game start failed!'})

        return result
