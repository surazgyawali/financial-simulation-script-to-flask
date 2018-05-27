
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
            jsonData = response.json()
            flask.session['sessionData'] = jsonData

        except requests.exceptions.RequestException as e:
            return redirect('/restart')

    try:
        response = requests.post(
            flask.request.url_root +'api/game',
            headers = {'sessid': flask.session['sessionData']['sessid']}
        )
        jsonData = response.json()
        return jsonData
    except requests.exceptions.RequestException as e:
        return redirect('/restart')

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
        jResponse = response.json()
        messages = jResponse['data']
        return messages
    except requests.exceptions.RequestException as e:
        ''' request exception'''
        return e
    except KeyError as e:
        '''key error'''
        return
    except Exception as e:
        '''uncatched exception'''
        return str(e)

def game_loop(header,messages=None):
    '''renders gameloop view with provided header parameter'''
    return render_template(
        'game.djhtml',
        messages   = messages,
        header     = header,
        sessid     = flask.session['sessionData']['sessid'],
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
        responseMessage = jsonData['data']
        return render_template(
            'game.djhtml',
            sessid     = flask.session['sessionData']['sessid'],
            header     = "On your command.",
            stats      = responseMessage[3:12],
            **gameLoopQuestions()
        )

    else:
        response = 0
        response = request.args.get('main')
        response = int(response)
        while response != 12:
            if response == 1:
                responseMessage = send_get_request('1')
                if not responseMessage:
                    return redirect('/error')
                print(responseMessage)
                return flask.render_template(
                    'hireFire.djhtml',
                    sessid     = flask.session['sessionData']['sessid'],
                    header     = "“Great vision without great people is irrelevant.",
                    messages   = ["How many underwriters would you like to hire or fire, choose suitably??"],
                    stats      = [responseMessage[0]],
                    question   = "The moment has come.",
                    uri        = 'game/1',
                    field_name = 'hire'
                )

            elif response == 2:
                responseMessage = send_get_request('2')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header     = "Platform Income Statement",
                    stats      = responseMessage[0:9],
                    messages   = ["Go on, what would you like to do now??"],
                    sessid     = flask.session['sessionData']['sessid'],
                    **gameLoopQuestions()
                )

            elif response == 3:
                responseMessage = send_get_request('3')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Platform Balance Sheet.",
                    sessid     = flask.session['sessionData']['sessid'],
                    stats    = responseMessage[0:7],
                    messages = ["Keep up the good business.What next??"],
                    **gameLoopQuestions()
                )

            elif response == 4:
                responseMessage = send_get_request('4')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Platform Cashflow statement.",
                    stats    = responseMessage[0:7],
                    sessid     = flask.session['sessionData']['sessid'],
                    messages = ["What will be your next command??"],
                    **gameLoopQuestions()
                )

            elif response == 5:
                responseMessage = send_get_request('5')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Loan Performance",
                    stats    = responseMessage[0:6],
                    sessid   = flask.session['sessionData']['sessid'],
                    messages = ["What would you like to do next ??"],
                    **gameLoopQuestions()
                )

            elif response == 6:
                responseMessage = send_get_request('6')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Loan buyer cash.",
                    stats    = responseMessage[0:3],
                    messages = ["What could be the next step to success??"],
                    sessid     = flask.session['sessionData']['sessid'],
                    **gameLoopQuestions()
                )

            elif response == 7:
                responseMessage = send_get_request('7')
                if not responseMessage:
                    return redirect('/error')
                purchased = responseMessage[0]
                if purchased:
                        return flask.render_template(
                            'game.djhtml',
                            header   = "Oops!!",
                            sessid     = flask.session['sessionData']['sessid'],
                            stats    = ["Buyer A already purchased. Please choose another option."],
                            messages = ["What would you like to do next ??"],
                            **gameLoopQuestions()
                )
                return flask.render_template(
                    'sellLoans.djhtml',
                    header     = "Let's sell some Loans.",
                    uri        = 'game/7',
                    sessid     = flask.session['sessionData']['sessid'],
                    question   = "How much would you like to sell (enter 0 to not sell)?",
                    warning    = responseMessage[1],
                    limit      = responseMessage[2],
                    field_name = "sell"
                )

            elif response == 8:
                responseMessage =  send_get_request('8')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'securitizeLoans.djhtml',
                    header     = "Let's Securitize some Loans.",
                    uri        = 'game/8',
                    sessid     = flask.session['sessionData']['sessid'],
                    info       = responseMessage[0:3],
                    question   = "How large would you like buyer D's tranche to be (enter 0 to not sell)?",
                    limit      = responseMessage[3],
                    field_name = "secure"
                )

            elif response == 9:
                responseMessage =  send_get_request('9')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'securitizeLoans.djhtml',
                    header     = "Sell into credit facility.",
                    uri        = 'game/9',
                    sessid     = flask.session['sessionData']['sessid'],
                    info       = [responseMessage[0]],
                    question   = "How much would you like to sell (enter 0 to not sell)?",
                    limit      = responseMessage[1],
                    field_name = 'sellFacility'
                )
            elif response == 10:
                return "TODO: Wil be here soon."

            elif response == 11:
                responseMessage =  send_get_request('11')
                if not responseMessage:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Credit Facility Info",
                    sessid     = flask.session['sessionData']['sessid'],
                    stats    = responseMessage[0:4],
                    messages = ["What would you like to do next ??"],
                    **gameLoopQuestions()
                )
            elif response == 13:
                responseMessage = send_get_request('13')
                if not responseMessage:
                    return flask.redirect('/restart')
                return flask.redirect('/restart')
        responseMessage =  send_get_request('12')
        return render_template(
            'game.djhtml',
            header     = "Congratulations.",
            sessid     = flask.session['sessionData']['sessid'],
            stats      = responseMessage[0:7],
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
    flask.session.clear()
    return redirect('/')

@app.route('/error')
def error():
    return render_template(
        'error.djhtml',
        header   = 'Uh oh!!! :(',
        messages = ['Sorry, Something went wrong.','Please restart the game.'],
        blabel   = "Why not??",
        id       = "gameStart"
        )