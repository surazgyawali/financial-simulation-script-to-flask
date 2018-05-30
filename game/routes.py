import requests

import flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from game.app import app
from game.utils import *


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
        responseWelcome = send_post_request()
        if not responseWelcome:
            return redirect('/restart')
        return render_template(
            'game.djhtml',
            sessid     = flask.session['sessionData']['sessid'],
            header     = "On your command.",
            stats      = responseWelcome[3:12],
            **gameLoopQuestions()
        )

    else:
        response = None
        response = request.args.get('main')
        response = int(response)
        while response != 12:
            if response == 1:
                responseHireFire = send_get_request('1')
                if not responseHireFire:
                    return redirect('/error')
                return flask.render_template(
                    'hireFire.djhtml',
                    header     = "“Great vision without great people is irrelevant.",
                    messages   = ["How many underwriters would you like to hire or fire, choose suitably??"],
                    stats      = [responseHireFire[0]],
                    question   = "The moment has come.",
                    uri        = 'game/1',
                    field_name = 'hire',
                    sessid     = flask.session['sessionData']['sessid']
                )

            elif response == 2:
                responsePIS = send_get_request('2')
                if not responsePIS:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header     = "Platform Income Statement",
                    stats      = responsePIS[0:9],
                    messages   = ["Go on, what would you like to do now??"],
                    sessid     = flask.session['sessionData']['sessid'],
                    **gameLoopQuestions()
                )

            elif response == 3:
                responsePBS = send_get_request('3')
                if not responsePBS:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Platform Balance Sheet.",
                    sessid     = flask.session['sessionData']['sessid'],
                    stats    = responsePBS[0:7],
                    messages = ["Keep up the good business.What next??"],
                    **gameLoopQuestions()
                )

            elif response == 4:
                responsePCS = send_get_request('4')
                if not responsePCS:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Platform Cashflow statement.",
                    stats    = responsePCS[0:7],
                    sessid     = flask.session['sessionData']['sessid'],
                    messages = ["What will be your next command??"],
                    **gameLoopQuestions()
                )

            elif response == 5:
                responseLoanPerformance = send_get_request('5')
                if not responseLoanPerformance:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Loan Performance",
                    stats    = responseLoanPerformance[0:6],
                    sessid   = flask.session['sessionData']['sessid'],
                    messages = ["What would you like to do next ??"],
                    **gameLoopQuestions()
                )

            elif response == 6:
                responseLBC = send_get_request('6')
                if not responseLBC:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Loan buyer cash.",
                    stats    = responseLBC[0:3],
                    messages = ["What could be the next step to success??"],
                    sessid     = flask.session['sessionData']['sessid'],
                    **gameLoopQuestions()
                )

            elif response == 7:
                responseSellLoans = send_get_request('7')
                if not responseSellLoans:
                    return redirect('/error')
                purchased = responseSellLoans[0]
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
                    warning    = responseSellLoans[1],
                    limit      = responseSellLoans[2],
                    field_name = "sell"
                )

            elif response == 8:
                responseSecuritizeLoans =  send_get_request('8')
                if not responseSecuritizeLoans:
                    return redirect('/error')
                return flask.render_template(
                    'securitizeLoans.djhtml',
                    header     = "Let's Securitize some Loans.",
                    uri        = 'game/8',
                    sessid     = flask.session['sessionData']['sessid'],
                    info       = responseSecuritizeLoans[0:3],
                    question   = "How large would you like buyer D's tranche to be (enter 0 to not sell)?",
                    limit      = responseSecuritizeLoans[3],
                    field_name = "secure"
                )

            elif response == 9:
                responseSellIntoCreditFacility =  send_get_request('9')
                if not responseSellIntoCreditFacility:
                    return redirect('/error')
                return flask.render_template(
                    'securitizeLoans.djhtml',
                    header     = "Sell into credit facility.",
                    uri        = 'game/9',
                    sessid     = flask.session['sessionData']['sessid'],
                    info       = [responseSellIntoCreditFacility[0]],
                    question   = "How much would you like to sell (enter 0 to not sell)?",
                    limit      = responseSellIntoCreditFacility[1],
                    field_name = 'sellFacility'
                )
            elif response == 10:
                return "TODO: Wil be here soon."

            elif response == 11:
                responseCFI =  send_get_request('11')
                if not responseCFI:
                    return redirect('/error')
                return flask.render_template(
                    'game.djhtml',
                    header   = "Credit Facility Info",
                    sessid     = flask.session['sessionData']['sessid'],
                    stats    = responseCFI[0:4],
                    messages = ["What would you like to do next ??"],
                    **gameLoopQuestions()
                )
            elif response == 13:
                responseQuit = send_get_request('13')
                return flask.redirect('/restart')

        responseNextQuarter =  send_get_request('12')
        if not responseNextQuarter:
            return flask.redirect('/restart')
        return render_template(
            'game.djhtml',
            header     = "Congratulations.",
            sessid     = flask.session['sessionData']['sessid'],
            stats      = responseNextQuarter[0:7],
            **gameLoopQuestions()
        )

@app.route('/game/1')
def game_hire():
    responseHire = request.args.get('hire')
    jsonData = send_get_request(responseHire)
    return game_loop(header = "Bingo,Some HR stuff has been done.", messages = ["Let's continue the pace."])


@app.route('/game/7')
def game_sell():
    responseSell = request.args.get('sell')
    jsonData = send_get_request(responseSell)
    return game_loop("Transaction successfully completed.Cheers :)",['So good so far.'])


@app.route('/game/8')
def game_perform_securitization():
    responseSecure = request.args.get('secure')
    jsonData = send_get_request(responseSecure)
    return game_loop("You've done it.",['"Beware of little expenses. A small leak will sink a great ship."\n- B.Frank', "Go on."])

@app.route('/game/9')
def game_perform_credit_sell():
    responseSellFacility = request.args.get('sellFacility')
    jsonData = send_get_request(responseSellFacility)
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