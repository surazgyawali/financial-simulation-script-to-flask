
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
            return redirect('/restart')
        jsonData = response.json()
        flask.session['sessionData'] = jsonData

    try:
        response = requests.post(
            flask.request.url_root +'api/game',
            headers = {'sessid': flask.session['sessionData']['sessid']}
        )
    except requests.exceptions.RequestException as e:
        return redirect('/restart')
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

@app.route('/game',methods = ['GET','POST'])
def gameStart():
    if request.method == 'POST':
        jsonData = send_post_request()
        messages = jsonData['data']
        return render_template(
            'game.djhtml',
            header     = "On your command.",
            # messages  = messages[0:3],
            stats      = messages[3:12],
            **gameLoopQuestions()
        )

    else:
        response = 0
        response = request.args.get('main')
        response = int(response)
        while response != 12:
            if response == 1:
                jResponse = send_get_request('1')
                messages = jResponse['data']
                return flask.render_template(
                    'hireFire.djhtml',
                    header     = "“Great vision without great people is irrelevant.",
                    messages   = [messages[1]],
                    stats      = [messages[0]],
                    question   = "The moment has come.",
                    uri        = 'game/1',
                    field_name = 'hire'
                )

            elif response == 2:
                jResponse = send_get_request('2')
                messages=jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    header     = "Platform Income Interest",
                    stats      = messages[0:9],
                    messages   = [messages[9]],
                    options    = messages[10:len(messages)-1],
                    question   = messages[len(messages)-1],
                    uri        = '/game',
                    field_name = 'main',
                )
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
                # jResponse = send_get_request('13')
                return flask.redirect('/restart')

@app.route('/game/1')
def game_hire():
    response = None
    response = request.args.get('hire')
    jsonData = send_get_request(response)
    return game_loop("Some RecruitMent has been done.Keep Going.")

@app.route('/restart')
def restart():
    flask.flash("You successfully retired.",category='success')
    flask.session.clear()
    return redirect('/')