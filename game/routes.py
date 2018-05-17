
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

def game_loop(header,messages=None):
    '''renders gameloop view with provided header parameter'''
    return render_template(
        'game.djhtml',
        messages   = messages,
        header     = header,
        **gameLoopQuestions()
    )

def gameLoopQuestions():
    'returns game loop questions in json/dict format'
    return{
            "options"   : [
                            '1:Hire/fire underwriters.',
                            '2:Check platform income statement.',
                            '3:Check platform balance sheet.',
                            '4:Check platform cash flow statement.',
                            '5:Check loan performance.',
                            '6:Check loan buyer cash.',
                            '7:Sell loans.',
                            '8:Securitize loans.',
                            '9:Sell into credit facility.',
                            '10:Refinance credit facility.',
                            '11:Credit facility info.',
                            '12:Move to next quarter.',
                            '13:Quit.'
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
                    **gameLoopQuestions()
                )

            elif response == 3:
                jResponse = send_get_request('3')
                messages = jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    stats    = messages[0:7],
                    messages = [messages[7]],
                    **gameLoopQuestions()
                )

            elif response == 4:
                jResponse = send_get_request('4')
                messages = jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    stats    = messages[0:7],
                    messages = [messages[7]],
                    **gameLoopQuestions()
                )

            elif response == 5:
                jResponse = send_get_request('5')
                messages  = jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    stats    = messages[0:6],
                    messages = [messages[6]],
                    **gameLoopQuestions()
                )

            elif response == 6:
                jResponse = send_get_request('6')
                messages  = jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    stats    = messages[0:3],
                    messages = [messages[3]],
                    **gameLoopQuestions()
                )

            elif response == 7:
                jResponse = send_get_request('7')
                messages  = jResponse['data']
                question  = messages[2]
                warning   = messages[0]
                limit     = messages[1]
                return flask.render_template(
                    'sellLoans.djhtml',
                    header     = "Let's sell some Loans.",
                    uri        = 'game/7',
                    question   = messages[2],
                    warning    = messages[0],
                    limit      = messages[1],
                    field_name = "sell"
                )

            elif response == 8:
                jResponse = send_get_request('8')
                messages = jResponse['data']
                return flask.render_template(
                    'securitizeLoans.djhtml',
                    header     = "Let's Securitize some Loans.",
                    uri        = 'game/8',
                    info       = messages[0:3],
                    question   = messages[4],
                    limit      = messages[3],
                    field_name = "secure"
                )

            elif response == 9:
                jResponse = send_get_request('9')
                messages  = jResponse['data']
                return flask.render_template(
                    'securitizeLoans.djhtml',
                    header     = "Sell into credit facility.",
                    uri        = 'game/9',
                    info       = [messages[0]],
                    question   = messages[2],
                    limit      = messages[1],
                    field_name = 'sellFacility'
                )
            elif response == 10:
                return "TODO: Wil be here soon."

            elif response == 11:
                jResponse = send_get_request('11')
                messages  = jResponse['data']
                return flask.render_template(
                    'game.djhtml',
                    stats    = messages[0:4],
                    messages = ["What would you like to do next ??"],
                    **gameLoopQuestions()
                )
            elif response == 13:
                jResponse = send_get_request('13')
                return flask.redirect('/restart')
        jResponse = send_get_request('12')
        messages   = jResponse['data']
        return render_template(
            'game.djhtml',
            header     = "Congratulations.",
            stats      = messages[0:7],
            **gameLoopQuestions()
        )

@app.route('/game/1')
def game_hire():
    response = request.args.get('hire')
    jsonData = send_get_request(response)
    return game_loop(header = "Bingo,Some HR stuff has been done.", messages = ["Let's continue the pace."])


@app.route('/game/7')
def game_sell():
    response = request.args.get('sell')
    jsonData = send_get_request(response)
    return game_loop("Transaction successfully completed.Cheers :)",['So good so far.'])


@app.route('/game/8')
def game_perform_securitization():
    response = request.args.get('secure')
    jsonData = send_get_request(response)
    return game_loop("You've done it.",['"Beware of little expenses. A small leak will sink a great ship."\n- B.Frank', "Go on."])

@app.route('/game/9')
def game_perform_credit_sell():
    response = request.args.get('sellFacility')
    jsonData = send_get_request(response)
    return game_loop("As your wish.",['"The longer I go on, the more I am aware of the power of finance. - J.W"', 'What would you like to do next??'])

@app.route('/restart')
def restart():
    flask.flash("You successfully retired.",category='success')
    flask.session.clear()
    return redirect('/')