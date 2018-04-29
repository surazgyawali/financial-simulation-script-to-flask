
import requests

import flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from game.app import app


def send_post_request():
    if flask.session.get('sessionData') is None:
        try:
            response = requests.post(
                flask.request.url_root +'api/game',
            )
        except requests.exceptions.RequestException as e:
            return e

        jsonData = response.json()
        flask.session['sessionData'] = jsonData

    try:
        response = requests.post(
            flask.request.url_root +'api/game',
            headers = {'sessid': flask.session['sessionData']['sessid']}
        )
    except requests.exceptions.RequestException as e:
        return e
    jsonData = response.json()
    return jsonData

def send_get_request(response):
    '''returns gamedata when passed response'''
    headerData = {
        'sessid'  : flask.session['sessionData']['sessid'],
        'message' : response
    }
    try:
        response = requests.get(
                    flask.request.url_root +'api/game',
                    headers = headerData
                )
    except requests.exceptions.RequestException as e:
        return e
    jResponse = response.json()
    return jResponse

def game_loop(header):
    '''renders gameloop view with provided header parameter'''
    return render_template(
        'game.djhtml',
        header     = header,
        **gameLoopQuestions()
    )

def gameLoopQuestions():
    'returns game loop questions in json/dict format'
    return{
            "options"   : ['Hire/fire underwriters.',
                            'Check platform income statement.',
                            'Check platform balance sheet.',
                            'Check platform cash flow statement.',
                            'Check loan performance.',
                            'Check loan buyer cash.',
                            'Sell loans.',
                            'Securitize loans.',
                            'Sell into credit facility.',
                            'Refinance credit facility.',
                            'Credit facility info.',
                            'Move to next quarter.',
                            'Quit.'
                        ],
            "question"  : 'Make a decision',
            "uri"       :'/game',
            "field_name": 'main',
    }


@app.route('/')
@app.route('/index')
def index():
    flask.session.clear()
    return flask.render_template(
        'welcome.djhtml',
        header   = 'Greetings!!!',
        messages = ['Want to be a CEO and manage a company??','You are just a click away.'],
        blabel   = "Let's play!",

        intro    = ["You are the CEO at a small start up lending platform, 'BestLending Inc.'",
                    "Your job is to ensure the growth of the platform to profitability.",
                    "Do this by managing the speed you grow the platform and choosing the best method of funding to minimize your company's Weighted Average Cost of Capital (WACC)."
                    ],
        introHeader = "Hi There!!!!",
        introBlabel   = "Next >>",
        id       = 'gameStart'
    )

@app.route('/main', methods = ['GET'])
def introPage():
    #To Do, put buyers and securitization buyers in array
    return flask.render_template(
        'game.djhtml',
        header   = "Hi There!!!",
        messages = [
                    "You are the CEO at a small start up lending platform, 'BestLending Inc.'",
                    "Your job is to ensure the growth of the platform to profitability.",
                    "Do this by managing the speed you grow the platform and choosing the best method of funding to minimize your company's Weighted Average Cost of Capital (WACC)."
                ],
        blabel   = "Next >>",
    )

@app.route('/game',methods = ['GET','POST'])
def gameStart():
    if request.method == 'POST':
        if flask.session.get('sessionData') is None:
            data = requests.post(
                flask.request.url_root +'api/game',
            )
            jsonData = data.json()
            flask.session['sessionData'] = jsonData


        data = requests.post(
            flask.request.url_root +'api/game',
            headers = {'sessid': flask.session['sessionData']['sessid']}
        )
        jsonData = data.json()
        flask.session['sessionData'] = jsonData
        messages = jsonData['data']
        sessid = jsonData['sessid']
        return flask.render_template(
            'game.djhtml',
            header     = "On your command.",
            # messages  = messages[0:3],
            stats      = messages[3:12],
            options    = messages[12:len(messages)-1],
            question   = messages[len(messages)-1],
            uri        = '/game',
            field_name = 'main',
        )

    if request.method == 'GET':
        response = 0
        response = request.args.get('main')
        headerData = {
            'sessid'  : flask.session['sessionData']['sessid'],
            'message' : response
        }
        print(flask.session['sessionData']['sessid'])
        print(headerData)
        response = int(response)
        while response != 12:
            if response == 1:
                jResponse = requests.get(
                    flask.request.url_root +'api/game',
                    headers = headerData
                ).json()
                messages = jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    header     = "“Great vision without great people is irrelevant.",
                    messages   = messages + ['Be careful: You have  to maintain the rate of contract as well as hire i.e the value could only be between -5 to 10.'],
                    options    = [i for i in range(-5,11)],
                    question   = "The moment has come.",
                )
            elif response == 2:
                return "TODO: The task."
            elif response == 3:
                return "TODO: The task."
            elif response == 4:
                return "TODO: The task."
            elif response == 5:
                return "TODO: The task."
            elif response == 6:
                return "TODO: The task."
            elif response == 7:
                return "TODO: The task."
            elif response == 8:
                return "TODO: The task."
            elif response == 9:
                return "TODO: The task."
            elif response == 10:
                return "TODO: The task."
            elif response == 11:
                return "TODO: The task."
            elif response == 13:
                flask.flash('You sucessfully retired!!!',category='success')
                flask.session.clear()
                return redirect(url_for('.index'))