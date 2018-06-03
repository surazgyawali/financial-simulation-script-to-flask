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
    if flask.session.get('sessionData'):
        sessionId = flask.session['sessionData']['sessid']
    sessionId = None
    return flask.render_template(
        'welcome.djhtml',
        header   = 'Greetings!!!',
        messages = ['Want to be a CEO and manage a company??','You are just a click away.'],
        blabel   = "Let's play!",

        intro    = ["You are the CEO at a small start up lending platform, 'BestLending Inc.'",
                    "Your job is to ensure the growth of the platform to profitability.",
                    "Do this by managing the speed you grow the platform and choosing the best method of funding to minimize your company's Weighted Average Cost of Capital (WACC)."
                    ],
        sessid   = sessionId,
        introHeader = "Hi There!!!!",
        introBlabel   = "Next >>",
        id       = 'gameStart'
    )

@app.route('/game',methods = ['GET','POST'])
def gameStart():
    if request.method == 'POST':
        responseWelcome = send_post_request()
        if validateResponse(responseWelcome):
            return redirect(url_for('main',dataWelcome = str(responseWelcome[3:12])))
        return redirect('/error')
    else:
        response = None
        response = request.args.get('main')
        response = int(response)

        while response != 12:
            if response == 1:
                responseHireFire = send_get_request('1')
                if validateResponse(responseHireFire):
                    return redirect(url_for('hireFire', dataHireFire = str(responseHireFire[0])))
                return redirect('/error')

            elif response == 2:
                responsePIS = send_get_request('2')
                if validateResponse(responsePIS):
                    return redirect(url_for('platformIncomeStatement', dataPIS = str(responsePIS[0:9])))
                return redirect('/error')

            elif response == 3:
                responsePBS = send_get_request('3')
                if validateResponse(responsePBS):
                    return redirect(url_for('platformBalanceSheet', dataPBS = str(responsePBS[0:7])))
                return redirect('/error')

            elif response == 4:
                responsePCS = send_get_request('4')
                if validateResponse(responsePCS):
                    return redirect(url_for('platformCashflowStatement', dataPCS = str(responsePCS[:7])))
                return redirect('/error')

            elif response == 5:
                responseLoanPerformance = send_get_request('5')
                if validateResponse(responseLoanPerformance):
                    return redirect(url_for('loanPerformance', dataLP = str(responseLoanPerformance[0:6])))
                return redirect('/error')

            elif response == 6:
                responseLBC = send_get_request('6')
                if validateResponse(responseLBC):
                    return redirect(url_for('loanBuyerCash', dataLBC = str(responseLBC[0:3])))
                return redirect('/error')

            elif response == 7:
                responseSellLoans = send_get_request('7')
                if validateResponse(responseSellLoans):
                    return redirect(url_for('sellLoans', dataSL = str(responseSellLoans[0:4])))
                return redirect('/error')

            elif response == 8:
                responseSecuritizeLoans =  send_get_request('8')
                if validateResponse(responseSecuritizeLoans):
                    return redirect(url_for('securitizeLoans', dataSecuritizeLoans = str(responseSecuritizeLoans[0:4])))
                return redirect('/error')

            elif response == 9:
                responseSellIntoCreditFacility =  send_get_request('9')
                if validateResponse(responseSellIntoCreditFacility):
                    return redirect(url_for('sellIntoCreditFacility', dataSICF = str(responseSellIntoCreditFacility[0:1])))
                return redirect('/error')

            elif response == 10:
                return "TODO: Wil be here soon."

            elif response == 11:
                responseCFI =  send_get_request('11')
                if validateResponse(responseCFI):
                    return redirect(url_for('creditFacilityInfo', dataCFI = str(responseCFI[0:4])))
                return redirect('/error')

            elif response == 13:
                return flask.redirect('/quit')

        responseNQ =  send_get_request('12')
        if validateResponse(responseNQ):
            return redirect(url_for('nextQuarter', dataNQ = str(responseNQ[0:7])))
        return redirect('/error')

@app.route('/game/hire-fire')
def game_hire():
    responseHire = request.args.get('hire')
    responseMessageHire = send_get_request(responseHire)
    return game_loop(header = "Bingo,Some HR stuff has been done.", messages = ["Let's continue the pace."])


@app.route('/game/sell-loans')
def game_sell():
    responseSell = request.args.get('sell')
    responseMessageSell = send_get_request(responseSell)
    return game_loop("Transaction successfully completed.Cheers :)",['So good so far.'])


@app.route('/game/securitize-loans')
def game_perform_securitization():
    responseSecure = request.args.get('secure')
    responseMessageSecure = send_get_request(responseSecure)
    return game_loop("You've done it.",['"Beware of little expenses. A small leak will sink a great ship."\n- B.Frank', "Go on."])


@app.route('/game/sell-into-credit-facility')
def game_perform_credit_sell():
    responseSellFacility = request.args.get('sellFacility')
    responseMessageSellFacility = send_get_request(responseSellFacility)
    return game_loop("As your wish.",['"The longer I go on, the more I am aware of the power of finance. - J.W"', 'What would you like to do next??'])


@app.route('/restart')
def restart():
    flask.session.clear()
    return redirect('/')


@app.route('/error')
def error():
    if flask.session.get('sessionData'):
        sessionId = flask.session['sessionData']['sessid']
    flask.session.clear()
    return render_template(
        'error.djhtml',
        header   = 'Uh oh!!! :(',
        messages = ['Sorry, Something went wrong.','Please restart the game.'],
        blabel   = "Why not??",
        id       = "gameStart",
        sessid   = sessionId
        )


@app.route('/hire-fire/<dataHireFire>')
def hireFire(dataHireFire):
        return flask.render_template(
            'hireFire.djhtml',
            header     = "“Great vision without great people is irrelevant.",
            messages   = ["How many underwriters would you like to hire or fire, choose suitably??"],
            stats      = [dataHireFire],
            question   = "The moment has come.",
            uri        = '/game/hire-fire',
            field_name = 'hire',
            sessid     = flask.session['sessionData']['sessid']
        )


@app.route('/platform-income-statement/<dataPIS>')
def platformIncomeStatement(dataPIS):
    return flask.render_template(
        'game.djhtml',
        header     = "Platform Income Statement",
        stats      = eval(dataPIS),
        messages   = ["Go on, what would you like to do now??"],
        sessid     = flask.session['sessionData']['sessid'],
        **gameLoopQuestions()
    )


@app.route('/platform-balance-sheet/<dataPBS>')
def platformBalanceSheet(dataPBS):
    return flask.render_template(
        'game.djhtml',
        header   = "Platform Balance Sheet.",
        sessid     = flask.session['sessionData']['sessid'],
        stats    = eval(dataPBS),
        messages = ["Keep up the good business.What next??"],
        **gameLoopQuestions()
    )


@app.route('/platform-cashflow-statement/<dataPCS>')
def platformCashflowStatement(dataPCS):
    return flask.render_template(
        'game.djhtml',
        header   = "Platform Cashflow statement.",
        stats    = eval(dataPCS),
        sessid     = flask.session['sessionData']['sessid'],
        messages = ["What will be your next command??"],
        **gameLoopQuestions()
    )


@app.route('/loan-performance/<dataLP>')
def loanPerformance(dataLP):
    return flask.render_template(
        'game.djhtml',
        header   = "Loan Performance",
        stats    = eval(dataLP),
        sessid   = flask.session['sessionData']['sessid'],
        messages = ["What would you like to do next ??"],
        **gameLoopQuestions()
    )


@app.route('/loan-buyer-cash/<dataLBC>')
def loanBuyerCash(dataLBC):
    return flask.render_template(
        'game.djhtml',
        header   = "Loan buyer cash.",
        stats    = eval(dataLBC),
        messages = ["What could be the next step to success??"],
        sessid     = flask.session['sessionData']['sessid'],
        **gameLoopQuestions()
    )


@app.route('/sell-loans/<dataSL>')
def sellLoans(dataSL):
    responseSellLoans = eval(dataSL)
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
        uri        = '/game/sell-loans',
        sessid     = flask.session['sessionData']['sessid'],
        question   = "How much would you like to sell (enter 0 to not sell)?",
        warning    = responseSellLoans[1],
        limit      = responseSellLoans[2],
        field_name = "sell"
    )

@app.route('/securitize-loans/<dataSecuritizeLoans>')
def securitizeLoans(dataSecuritizeLoans):
    return flask.render_template(
        'securitizeLoans.djhtml',
        header     = "Let's Securitize some Loans.",
        uri        = '/game/securitize-loans',
        sessid     = flask.session['sessionData']['sessid'],
        info       = eval(dataSecuritizeLoans),
        question   = "How large would you like buyer D's tranche to be (enter 0 to not sell)?",
        field_name = "secure"
    )

@app.route('/sell-into-credit-facility/<dataSICF>')
def sellIntoCreditFacility(dataSICF):
    return flask.render_template(
        'securitizeLoans.djhtml',
        header     = "Sell into credit facility.",
        uri        = '/game/sell-into-credit-facility',
        sessid     = flask.session['sessionData']['sessid'],
        question   = "How much would you like to sell (enter 0 to not sell)?",
        info      = eval(dataSICF),
        field_name = 'sellFacility'
    )


@app.route('/credit-facility-info/<dataCFI>')
def creditFacilityInfo(dataCFI):
    return flask.render_template(
        'game.djhtml',
        header   = "Credit Facility Info",
        sessid     = flask.session['sessionData']['sessid'],
        stats    = eval(dataCFI),
        messages = ["What would you like to do next ??"],
        **gameLoopQuestions()
    )


@app.route('/quit')
def quit():
    responseQuit = send_get_request('13')
    flask.session.clear()
    return redirect('/')


@app.route('/next-quarter/<dataNQ>')
def nextQuarter(dataNQ):
    return render_template(
        'game.djhtml',
        header     = "Congratulations.",
        sessid     = flask.session['sessionData']['sessid'],
        stats      = eval(dataNQ),
        **gameLoopQuestions()
    )


@app.route('/main/<dataWelcome>')
def main(dataWelcome):
    return render_template(
        'game.djhtml',
        header     = "On your command.",
        stats      = eval(dataWelcome),
        sessid     = flask.session['sessionData']['sessid'],
        **gameLoopQuestions()
    )