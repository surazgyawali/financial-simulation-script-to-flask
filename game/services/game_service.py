import time
from flask import current_app as app
from threading import Thread, Lock
from .helper import *

class GameService(Thread):
    def __init__(self, sessid):
        '''Initializes parameters for background thread processing'''
        super(GameService, self).__init__()

        self.sessid = sessid
        self.in_queue = app.in_queue
        self.out_queue = app.out_queue
        self.queue_key = app.config['QUEUE_KEY']

        self.message = []
        self.lock = None

        self.daemon = True
        self.cancelled = False

    def init_game(self):
        '''Initializes the game'''
        try:
            pass
        except Exception as e:
            return -1, dict({'result': 'Game initialization error!'})

        return 0, dict({'result' : 'Game initialization complete'})

    def cancel(self):
        self.cancelled = True

    def post_message(self):
        '''Puts the message and current query in outbound queue'''
        key = '{}:{}'.format(self.queue_key, self.sessid)
        value = self.message
        self.lock.acquire()
        self.out_queue[self.sessid][key] = value
        self.lock.release()
        self.message = []

    def get_message(self):
        '''Gets the current response from inbound queue'''
        key = '{}:{}'.format(self.queue_key, self.sessid)
        if not self.in_queue.get(self.sessid, None):
            return None
        retry_count = 5
        for _ in range(retry_count):
            value = self.in_queue[self.sessid].get(key, None)
            if value is not None:
                status = 0
                break
            else:
                time.sleep(1)
                continue
        if value is None:
            status = -1
        else:
            self.in_queue[self.sessid] = {}
        return value

    def run(self):
        '''Runs a background task to execute game steps'''
        if not self.in_queue.get(self.sessid, None):
            self.in_queue[self.sessid] = {}
        if not self.out_queue.get(self.sessid, None):
            self.out_queue[self.sessid] = {}
        self.lock = Lock()
        while not self.cancelled:
            #try:

            self.gameStart()

            #except Exception as exception:
            #	print 'Exception encountered: {}'.format(exception)
            #	self.cancelled = True

    def gameStart(self):
        self.message = []
        self.message.append("You are the CEO at a small start up lending platform, 'BestLending Inc.'")
        self.message.append("Your job is to ensure the growth of the platform to profitability.")
        self.message.append(
        "Do this by managing the speed you grow the platform and choosing the best method of funding to minimize your company's Weighted Average Cost of Capital (WACC).")

        # To Do, put buyers and securitization buyers in arrays
        a = Buyer()
        b = Buyer()
        d = TrancheBuyer()
        e = TrancheBuyer()
        f = Facility()

        c = Company(f)
        while True:
            economy = randint(-4, 5)
            ret = self.gameLoop(a, b, c, d, e, f, economy)
            if ret == 1:
                break
        return c

    def gameLoop(self, a, b, c, d, e, f, economy):
        # Game loop should ask player for response.
        # Choose various settings like origination growth or financing
        # Then run company step function

        if c.quarter > 4:
            c.quarter = 1
            c.year += 1

        date_string = 'Q' + str(c.quarter) + ' ' + str(c.year) + '.'

        self.message.append("Your quarterly results came in for {}".format(date_string))
        self.message.append("The economy strength is: {}".format(economy))
        self.message.append("The net income was: {}".format(round(c.netIncome,2)))
        self.message.append("Your cash is: {}".format(round(c.cash,2)))
        self.message.append("The platform originated new loan UPB of: {}".format(round(c.originations,2)))
        self.message.append("Your burnrate was: {}".format(round(c.burnRate,2)))
        self.message.append("Your runway is: {}".format(round(c.runway,2)))
        self.message.append("")

        # Reset the check if buyer a has purchased
        a.purchased = False

        # Get input from player
        response = 0
        while response != 12:
            self.message.append("What would you like to do?")
            self.message.append("1 :Hire/fire underwriters.")
            self.message.append("2 :Check platform income statement.")
            self.message.append("3 :Check platform balance sheet.")
            self.message.append("4 :Check platform cash flow statement.")
            self.message.append("5 :Check loan performance.")
            self.message.append("6 :Check loan buyer cash.")
            self.message.append("7 :Sell loans.")
            self.message.append("8 :Securitize loans.")
            self.message.append("9 :Sell into credit facility.")
            self.message.append("10:Refinance credit facility.")  # Still to do
            self.message.append("11:Credit facility info.")
            self.message.append("12:Move to next quarter.")
            self.message.append("13:Quit.")
            response = self.get_main_game_option("Make a decision")

            if response == 1:
                self.message.append("You have {} good, {} neutral, {} bad underwriters.".format( c.goodUW, c.UW, c.badUW))
                num = self.get_underwriters("How many underwriters would you like to hire (or fire)? ")
                c.addUnderwriters(num)
            elif response == 2:
                self.message.append("Interest income: {} {}".format(round(c.portfolio.interestIncome, 2),
                      round((c.portfolio.interestIncome - c.portfolio.realizedLosses) / c.portfolio.loanUPB * 100 * 4, 2)))
                self.message.append("Origination income: {}".format(round(c.originationFees,2)))
                self.message.append("Servicing income: {}".format(round(c.servicingFees,2)))
                self.message.append("Facility income: {}".format(round(f.div,2)))
                self.message.append("Residual income: {} {}".format(round(c.residualGain,2),round(c.residualGain / (c.residualInvestments + 0.01) * 100 * 4,2)))
                self.message.append("Reserve change: {}".format(round(c.reserveChange,2)))
                self.message.append("Corporate overhead: {}".format(-1 * (round(c.corporateOverhead + c.SGA,2))))
                self.message.append("Net Income: {}".format(round(c.netIncome,2)))
                self.message.append("")
            elif response == 3:
                self.message.append("Cash: {}".format(round(c.cash,2)))
                self.message.append("Loan UPB: {}".format(round(c.portfolio.loanUPB,2)))
                self.message.append("Loss Reserve: {}".format(round(c.lossReserve,2)))
                self.message.append("Residual Investments: {}".format(round(c.residualInvestments,2)))
                self.message.append("Facility Equity: {}".format(round(f.portfolio.loanUPB - f.loanSize,2)))
                self.message.append("Corporate Equity: {}".format(round(c.equity,2)))
                self.message.append("")
            elif response == 4:
                self.message.append("Originated UPB: {}".format(round(c.originations,2)))
                self.message.append("Sold UPB: {}".format(c.loanSales))
                self.message.append("Securitized UPB: {}".format(round(c.securitizedPrincipal,2)))
                self.message.append("Loan CF: {}".format(round(c.portfolio.interestIncome + c.portfolio.principalPayments,2)))
                self.message.append("Securitization CF: {}".format(round(c.residualPayments,2)))
                self.message.append("Total Cash Flow: {}".format(
                    round(c.residualPayments + c.portfolio.interestIncome + c.portfolio.principalPayments - c.originations,2)))
                self.message.append("")
            elif response == 5:
                if len(c.portfolio.loanYield) <= 3:
                    self.message.append("Portfolio too young to check yield")
                else:
                    self.message.append("Yield: {}".format(round(sum(c.portfolio.loanYield) * 100),2))
                self.message.append("Realized loss: {} {}".format(round(c.portfolio.realizedLosses,2),
                      round(c.portfolio.realizedLosses / c.portfolio.loanUPB * 100 * 4,2)))
                self.message.append("Weighted Average Coupon: {}".format(round(c.portfolio.wavgCoupon,2)))
                self.message.append("Weighted Average Default Rate: {}".format(round(c.portfolio.wavgCDR,2)))
                self.message.append("Weighted Average Remaining Term: {}".format(round(c.portfolio.wavgRemTerm,2)))
                self.message.append("")
            elif response == 6:
                self.message.append("Buyer A cash:{} ".format(round(a.cash,2)))
                self.message.append("Buyer D cash:{} ".format(round(d.cash,2)))
                self.message.append("")
            elif response == 7:
                self.message.append(a.purchased)
                if a.purchased:
                    self.message.append("Buyer A already purchased. Please choose another option.")
                    self.message.append("")
                else:
                    self.perform_loan_sale(a, b, c, economy)
            elif response == 8:
                self.perform_securitization(c, d, e, economy)
            elif response == 9:
                self.addToFacility(c, f)
            elif response == 10:
                self.refiFacility(c, f, economy)
            elif response == 11:
                self.message.append("Facility size: {}".format(f.maxSize))
                self.message.append("Facility current size: {}".format(round(f.loanSize,2)))
                self.message.append("Facility portfolio size: {}".format(round(f.portfolio.loanUPB,2)))
                self.message.append("Last quarter facility cashflow: {}".format(round(f.div,4)))
                self.message.append("")
            elif response == 13:
                return 1

        a.portfolio.runLoans(economy)
        a.checkEmotions()

        # Assume each of these steps is quarterly
        c.originateLoans(economy)

        c.runResids(economy)
        d.updateHoldings()
        f.updateFacility(c, economy)

        c.updateIncomeStatement(economy)
        c.updateBalanceSheet()
        c.updateCashFlowStatement()

        c.quarter += 1

    def addToFacility(self, c, f):

        facilityLimit = (f.maxSize - f.loanSize) / f.advanceRate
        advanceLimit = min(facilityLimit, c.portfolio.loanUPB)
        self.message.append("The facility can accept {}".format(round(advanceLimit,2)))
        self.message.append(advanceLimit)

        while True:
            try:
                self.message.append("How much would you like to sell (enter 0 to not sell)? ")
                self.post_message()
                response = None
                while response == None:
                    response =  self.get_message()
                value = int(response)
            except ValueError:
                self.message.append("Sorry, I didn't understand that.")
                continue

            if value == 0:
                return
            elif value > c.portfolio.loanUPB:
                self.message.append("Sorry, you are not allowed to sell more than your portfolio.")
                continue
            elif value > advanceLimit:
                self.message.append("Sorry, you must sell less than the facility advance limit.")
                continue
            elif value < 0:
                self.message.append("Sorry, that is not a valid option.")
            else:
                break

        c.cash += value * f.advanceRate
        c.runway = c.cash / c.burnRate

        f.portfolio.addLoans(value, c.portfolio.wavgCoupon, c.portfolio.wavgCDR, newRemTerm=c.portfolio.wavgRemTerm)
        c.portfolio.sellLoans(value, c.portfolio.wavgCoupon, c.portfolio.wavgCDR)
        f.loanSize += value * f.advanceRate

    def perform_securitization(self, c, d, e, economy):
        desireSpreadD = 4 - economy / 2
        desireOvercollatD = 30 + economy * 5
        purchaseLimitD = min((d.confidence + 1) * 300, d.cash, c.portfolio.loanUPB * (1 - desireOvercollatD / 100))

        self.message.append("Buyer D can finance up to {}".format(round(purchaseLimitD,2)))
        self.message.append("Buyer D would like a yield of {}".format(round(desireSpreadD,2)))
        self.message.append("Buyer D would like overcollateralization of {}".format(desireOvercollatD))
        self.message.append(purchaseLimitD)

        while True:
            try:
                self.message.append("How large would you like buyer D's tranche to be (enter 0 to not sell)? ")
                self.post_message()
                response = None
                while response == None:
                    response =  self.get_message()
                value = int(response)
            except ValueError:
                self.message.append("Sorry, I didn't understand that.")
                continue

            if value == 0:
                return
            elif value > c.portfolio.loanUPB * (1 - desireOvercollatD / 100):
                self.message.append("Sorry, you are not allowed to finance more than your portfolio.")
                continue
            elif value > purchaseLimitD:
                self.message.append("Sorry, you must sell less than buyer D's purchase limit.")
                continue
            elif value < 0:
                self.message.append("Sorry, that is not a valid option.")
            else:
                break

        d.cash -= value
        c.cash += value
        c.runway = c.cash / c.burnRate

        t1 = Tranche(value, desireSpreadD / 100)
        sPort = Portfolio(0)
        sPort.addLoans(value / (1 - desireOvercollatD / 100), c.portfolio.wavgCoupon, c.portfolio.wavgCDR,
                        newRemTerm=c.portfolio.wavgRemTerm)

        finStruct = Structure([t1], sPort, 1 - desireOvercollatD / 100 - 0.1)
        c.portfolio.sellLoans(value / (1 - desireOvercollatD / 100), c.portfolio.wavgCoupon, c.portfolio.wavgCDR)

        c.residList.append(finStruct)
        c.residualInvestments += (value / (1 - desireOvercollatD / 100) - value)
        d.assets.append(t1)
        d.confidence += 1

    def perform_loan_sale(self, a, b, c, economy):
        purchaseLimitA = min((a.confidence + 1) * 200, a.cash, c.portfolio.loanUPB)

        self.message.append("Buyer A can buy up to {}".format(round(purchaseLimitA,2)))
        self.message.append(purchaseLimitA)

        while True:
            try:
                self.message.append("How much would you like to sell (enter 0 to not sell)? ")
                self.post_message()
                response = None
                while response == None:
                    response =  self.get_message()
                value = int(response)
            except ValueError:
                self.message.append("Sorry, I didn't understand that.")
                continue

            if value == 0:
                return
            elif value > c.portfolio.loanUPB:
                self.message.append("Sorry, you are not allowed to sell more than your portfolio.")
                continue
            elif value > purchaseLimitA:
                self.message.append("Sorry, you must sell less than buyer A's purchase limit.")
                continue
            elif value < 0:
                self.message.append("Sorry, that is not a valid option.")
            else:
                break
            '''else:
                try:
                    value = int(input("Who would you like to sell it to?"))
                except ValueError:
                    self.message.append("Sorry, I didn't understand that.")
                    continue'''

        a.cash -= value
        c.cash += value
        c.runway = c.cash / c.burnRate
        a.portfolio.addLoans(value, c.portfolio.wavgCoupon, c.portfolio.wavgCDR, newRemTerm=c.portfolio.wavgRemTerm)
        c.soldPortfolioA.addLoans(value, c.portfolio.wavgCoupon, c.portfolio.wavgCDR,
                                    newRemTerm=c.portfolio.wavgRemTerm)
        c.portfolio.sellLoans(value, c.portfolio.wavgCoupon, c.portfolio.wavgCDR, )

        a.purchased = True
        a.confidence += 1
        self.message.append("Successfully sold.")
        self.message.append("")

    def get_main_game_option(self, prompt):
        while True:
            try:
                self.message.append(prompt)
                self.post_message()
                response = None
                while response == None:
                    response =  self.get_message()
                value = int(response)
            except ValueError:
                self.message.append("Sorry, I didn't understand that.")
                continue

            if value < 1:
                self.message.append("Sorry, that is not a valid option.")
                continue
            elif value > 13:
                self.message.append("Sorry, that is not a valid option.")
            else:
                break
        return value

    # Various input functions
    def get_percentage_int(self, prompt):
        while True:
            try:
                self.message.append(prompt)
                self.post_message()
                response = None
                while response == None:
                    response =  self.get_message()
                value = int(response)
            except ValueError:
                self.message.append("Sorry, I didn't understand that.")
                continue

            if value < -25:
                self.message.append("Sorry, you cannot contract that fast.")
                continue
            elif value > 1000:
                self.message.append("Sorry, you cannot grow that fast. Please input a lower growth rate.")
            else:
                break
        return value

    def get_underwriters(self, prompt):
        while True:
            try:
                self.message.append(prompt)
                self.post_message()
                response = None
                while response == None:
                    response =  self.get_message()
                value = int(response)
            except ValueError:
                self.message.append("Sorry, I didn't understand that.")
                continue

            if value < -5:
                self.message.append("Sorry, you cannot contract that fast.")
                continue
            elif value > 10:
                self.message.append("Sorry, you cannot hire that fast. Please input a lower growth rate.")
            else:
                break
        return value
