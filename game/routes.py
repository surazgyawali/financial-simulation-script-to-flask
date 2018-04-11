from random import randint
import numpy as np

import flask
from flask import render_template


from game import app



@app.route('/static/<path:filepath>')
def serve_static(filename):
    return flask.url_for('static', filename)


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.djhtml',
    )

@app.route('/game')
def gameStart():
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
        href     = "/game/company"
    )

@app.route('/game/company')
def company():
    a = Buyer()
    b = Buyer()
    d = TrancheBuyer()
    e = TrancheBuyer()
    f = Facility()

    c = Company(f)
    # while True:
    economy = randint(-4,5)
    ret = gameLoop(a,b,c,d,e,f,economy)
    print(ret)
        # if ret == 1:
            # break
        # return str(c)
    return render_template(
        'game.djhtml',
        header   = "Company Details.",
        messages = ret,
        href     = '/',
        blabel   = "Next>>"
    )

def gameLoop(a,b,c,d,e,f,economy):
    #Game loop should ask player for response.
    #Choose various settings like origination growth or financing
    #Then run company step function

    if c.quarter > 4:
        c.quarter = 1
        c.year += 1

    date_string = 'Q'+str(c.quarter)+' '+str(c.year)+'.'

    companyDetails = [
    "Your quarterly results came in for "+str(date_string),
    "The economy strength is: "+str(economy),
    "The net income was: "+str(c.netIncome),
    "Your cash is: "+str(c.cash),
    "The platform originated new loan UPB of: "+str(c.originations),
    "Your burnrate was: "+str(c.burnRate),
    "Your runway is: "+str(c.runway),
    ]
    return companyDetails
