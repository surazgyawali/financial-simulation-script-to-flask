from random import randint
import numpy as np

import flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request


from game import app

from game.ctrl import *



@app.route('/')
@app.route('/index')
def index():
    flask.session['uid'] = randint(0,1000)
    return render_template(
        'game.djhtml',
        header   = 'Greetings!!!',
        messages = ['Want to be a CEO and manage a company??','You are just a click away.'],
        blabel   = "Let's play!",
        href     = "/welcome"
    )


@app.route('/welcome')
def introPage():
    #To Do, put buyers and securitization buyers in array
    return render_template(
        'game.djhtml',
        header   = "Hi There!!!",
        messages = [
                    "You are the CEO at a small start up lending platform, 'BestLending Inc.'",
                    "Your job is to ensure the growth of the platform to profitability.",
                    "Do this by managing the speed you grow the platform and choosing the best method of funding to minimize your company's Weighted Average Cost of Capital (WACC)."
                ],
        blabel   = "Next >>",
        href     = "/game"
    )


@app.route('/game',methods = ['GET','POST'])
def gameStart():
    a = Buyer()
    b = Buyer()
    d = TrancheBuyer()
    e = TrancheBuyer()
    f = Facility()
    c = Company(f)
    economy = randint(-4,5)


    if c.quarter > 4:
        c.quarter = 1
        c.year += 1

    date_string = 'Q'+str(c.quarter)+' '+str(c.year)+'.'

    info = [
            "Your quarterly results came in for %s" % date_string,
            "The economy strength is: %d" %economy,
            "The net income was: %d"%c.netIncome,
            "Your cash is: %d"%c.cash,
            "The platform originated new loan UPB of: %d"%c.originations,
            "Your burnrate was: %d"%c.burnRate,
            "Your runway is: %d"%c.runway,
            ""
        ]

    if request.method == 'POST':
        response = 0
        response = int(request.form.get('selected'))
        print(response)
        while response != 12:
            if response == 1:
                return "TODO: Do The task."
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
                return redirect(url_for('.index'))
            #TODO: add missing conditions


        a.portfolio.runLoans(economy)
        a.checkEmotions()

        #Assume each of these steps is quarterly
        c.originateLoans(economy)

        c.runResids(economy)
        d.updateHoldings()
        f.updateFacility(c,economy)

        c.updateIncomeStatement(economy)
        c.updateBalanceSheet()
        c.updateCashFlowStatement()

        c.quarter += 1

    # check something and do something here

    #else show something else
    return render_template(
        'game.djhtml',
        header   = "On your command!!!",
        messages  = info,
        question  = "What Would you like to do???",
        options   = [
                        "Hire/fire underwriters.",
                        "Check platform income statement.",
                        "Check platform balance sheet.",
                        "Check platform cash flow statement.",
                        "Check loan performance.",
                        "Check loan buyer cash.",
                        "Sell loans.",
                        "Securitize loans.",
                        "Sell into credit facility.",
                        " Refinance credit facility.", #Still to do
                        " Credit facility info.",
                        " Move to next quarter.",
                        " Quit.",
                        ],
)