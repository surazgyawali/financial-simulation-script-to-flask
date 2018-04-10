#!/venv/bin/python3

from random import randint
import numpy as np


def gameStart():
    print("You are the CEO at a small start up lending platform, 'BestLending Inc.'")
    print("Your job is to ensure the growth of the platform to profitability.")
    print("Do this by managing the speed you grow the platform and choosing the best method of funding to minimize your company's Weighted Average Cost of Capital (WACC).")

    #To Do, put buyers and securitization buyers in arrays
    a = Buyer()
    b = Buyer()
    d = TrancheBuyer()
    e = TrancheBuyer()
    f = Facility()

    c = Company(f)
    while True:
        economy = randint(-4,5)
        ret = gameLoop(a,b,c,d,e,f,economy)
        if ret == 1:
            break
    return c


def gameLoop(a,b,c,d,e,f,economy):
    #Game loop should ask player for response.
    #Choose various settings like origination growth or financing
    #Then run company step function

    if c.quarter > 4:
        c.quarter = 1
        c.year += 1

    date_string = 'Q'+str(c.quarter)+' '+str(c.year)+'.'

    print("Your quarterly results came in for ",date_string)
    print("The economy strength is: ",economy)
    print("The net income was: ",c.netIncome)
    print("Your cash is: ",c.cash)
    print("The platform originated new loan UPB of: ",c.originations)
    print("Your burnrate was: ",c.burnRate)
    print("Your runway is: ",c.runway)
    print("")

    #Reset the check if buyer a has purchased
    a.purchased = False

    #Get input from player
    response = 0
    while response != 12:
        print("What would you like to do?")
        print("1: Hire/fire underwriters.")
        print("2: Check platform income statement.")
        print("3: Check platform balance sheet.")
        print("4: Check platform cash flow statement.")
        print("5: Check loan performance.")
        print("6: Check loan buyer cash.")
        print("7: Sell loans.")
        print("8: Securitize loans.")
        print("9: Sell into credit facility.")
        print("10: Refinance credit facility.") #Still to do
        print("11: Credit facility info.")
        print("12: Move to next quarter.")
        print("13: Quit.")
        response = get_main_game_option("Input the number you'd like: ")

        if response == 1:
            print("You have good, neutral, bad underwriters respectively: ",c.goodUW, c.UW, c.badUW)
            num = get_underwriters("How many underwriters would you like to hire (or fire)? ")
            c.addUnderwriters(num)
        elif response == 2:
            print("Interest income: ",c.portfolio.interestIncome, (c.portfolio.interestIncome-c.portfolio.realizedLosses)/c.portfolio.loanUPB*100*4)
            print("Origination income: ",c.originationFees)
            print("Servicing income: ",c.servicingFees)
            print("Facility income: ",f.div)
            print("Residual income: ",c.residualGain, c.residualGain/(c.residualInvestments+0.01)*100*4)
            print("Reserve change: ",c.reserveChange)
            print("Corporate overhead: ",-1*(c.corporateOverhead+c.SGA))
            print("Net Income: ", c.netIncome)
            print("")
        elif response == 3:
            print("Cash: ",c.cash)
            print("Loan UPB: ",c.portfolio.loanUPB)
            print("Loss Reserve: ",c.lossReserve)
            print("Residual Investments: ",c.residualInvestments)
            print("Facility Equity: ", f.portfolio.loanUPB - f.loanSize)
            print("Corporate Equity: ",c.equity)
            print("")
        elif response == 4:
            print("Originated UPB: ",c.originations)
            print("Sold UPB: ",c.loanSales)
            print("Securitized UPB: ",c.securitizedPrincipal)
            print("Loan CF: ",c.portfolio.interestIncome + c.portfolio.principalPayments)
            print("Securitization CF: ",c.residualPayments)
            print("Total Cash Flow: ",c.residualPayments+c.portfolio.interestIncome + c.portfolio.principalPayments-c.originations)
            print("")
        elif response == 5:
            if len(c.portfolio.loanYield) <= 3:
                print("Portfolio too young to check yield")
            else:
                print("Yield: ",sum(c.portfolio.loanYield)*100)
            print("Realized loss: ",c.portfolio.realizedLosses, c.portfolio.realizedLosses/c.portfolio.loanUPB*100*4)
            print("Weighted Average Coupon: ",c.portfolio.wavgCoupon)
            print("Weighted Average Default Rate: ",c.portfolio.wavgCDR)
            print("Weighted Average Remaining Term: ",c.portfolio.wavgRemTerm)
            print("")
        elif response == 6:
            print("Buyer A cash: ",a.cash)
            print("Buyer D cash: ",d.cash)
            print("")
        elif response == 7:
            if a.purchased:
                print("Buyer A already purchased. Please choose another option.")
                print("")
            else:
                perform_loan_sale(a,b,c,economy)
        elif response == 8:
            perform_securitization(c,d,e,economy)
        elif response == 9:
            addToFacility(c,f)
        elif response == 10:
            refiFacility(c,f,economy)
        elif response == 11:
            print("Facility size: ",f.maxSize)
            print("Facility current size: ",f.loanSize)
            print("Facility portfolio size: ",f.portfolio.loanUPB)
            print("Last quarter facility cashflow: ",f.div)
            print("")
        elif response == 13:
            return 1


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


def addToFacility(c,f):

    facilityLimit = (f.maxSize - f.loanSize)/f.advanceRate
    advanceLimit = min(facilityLimit, c.portfolio.loanUPB)
    print("The facility can accept ",advanceLimit)

    while True:
        try:
            value = int(input("How much would you like to sell (enter 0 to not sell)? "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value == 0:
            return
        elif value > c.portfolio.loanUPB:
            print("Sorry, you are not allowed to sell more than your portfolio.")
            continue
        elif value > advanceLimit:
            print("Sorry, you must sell less than the facility advance limit.")
            continue
        elif value < 0:
            print("Sorry, that is not a valid option.")
        else:
            break

    c.cash += value*f.advanceRate
    c.runway = c.cash / c.burnRate

    f.portfolio.addLoans(value,c.portfolio.wavgCoupon,c.portfolio.wavgCDR,newRemTerm=c.portfolio.wavgRemTerm)
    c.portfolio.sellLoans(value,c.portfolio.wavgCoupon,c.portfolio.wavgCDR)
    f.loanSize += value*f.advanceRate


def perform_securitization(c,d,e,economy):
    desireSpreadD = 4-economy/2
    desireOvercollatD = 30 + economy*5
    purchaseLimitD = min((d.confidence + 1) * 300,d.cash,c.portfolio.loanUPB*(1-desireOvercollatD/100))

    print("Buyer D can finance up to ",purchaseLimitD)
    print("Buyer D would like a yield of ",desireSpreadD)
    print("Buyer D would like overcollateralization of ",desireOvercollatD)

    while True:
        try:
            value = int(input("How large would you like buyer D's tranche to be (enter 0 to not sell)? "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value == 0:
            return
        elif value > c.portfolio.loanUPB*(1-desireOvercollatD/100):
            print("Sorry, you are not allowed to finance more than your portfolio.")
            continue
        elif value > purchaseLimitD:
            print("Sorry, you must sell less than buyer D's purchase limit.")
            continue
        elif value < 0:
            print("Sorry, that is not a valid option.")
        else:
            break

    d.cash -= value
    c.cash += value
    c.runway = c.cash / c.burnRate

    t1 = Tranche(value,desireSpreadD/100)
    sPort = Portfolio(0)
    sPort.addLoans(value/(1-desireOvercollatD/100),c.portfolio.wavgCoupon,c.portfolio.wavgCDR,newRemTerm=c.portfolio.wavgRemTerm)

    finStruct = Structure([t1],sPort,1-desireOvercollatD/100-0.1)
    c.portfolio.sellLoans(value/(1-desireOvercollatD/100),c.portfolio.wavgCoupon,c.portfolio.wavgCDR)

    c.residList.append(finStruct)
    c.residualInvestments += (value/(1-desireOvercollatD/100) - value)
    d.assets.append(t1)
    d.confidence += 1


def perform_loan_sale(a,b,c,economy):
    purchaseLimitA = min((a.confidence + 1) * 200,a.cash,c.portfolio.loanUPB)

    print("Buyer A can buy up to ",purchaseLimitA)

    while True:
        try:
            value = int(input("How much would you like to sell (enter 0 to not sell)? "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value == 0:
            return
        elif value > c.portfolio.loanUPB:
            print("Sorry, you are not allowed to sell more than your portfolio.")
            continue
        elif value > purchaseLimitA:
            print("Sorry, you must sell less than buyer A's purchase limit.")
            continue
        elif value < 0:
            print("Sorry, that is not a valid option.")
        else:
            break
        '''else:
            try:
                value = int(input("Who would you like to sell it to?"))
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue'''

    a.cash -= value
    c.cash += value
    c.runway = c.cash / c.burnRate
    a.portfolio.addLoans(value,c.portfolio.wavgCoupon,c.portfolio.wavgCDR,newRemTerm=c.portfolio.wavgRemTerm)
    c.soldPortfolioA.addLoans(value,c.portfolio.wavgCoupon,c.portfolio.wavgCDR,newRemTerm=c.portfolio.wavgRemTerm)
    c.portfolio.sellLoans(value,c.portfolio.wavgCoupon,c.portfolio.wavgCDR,)

    a.purchased = True
    a.confidence += 1
    print("Successfully sold.")
    print("")


def get_main_game_option(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value < 1:
            print("Sorry, that is not a valid option.")
            continue
        elif value > 13:
            print("Sorry, that is not a valid option.")
        else:
            break
    return value

#Various input functions
def get_percentage_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value < -25:
            print("Sorry, you cannot contract that fast.")
            continue
        elif value > 1000:
            print("Sorry, you cannot grow that fast. Please input a lower growth rate.")
        else:
            break
    return value

def get_underwriters(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value < -5:
            print("Sorry, you cannot contract that fast.")
            continue
        elif value > 10:
            print("Sorry, you cannot hire that fast. Please input a lower growth rate.")
        else:
            break
    return value




class Portfolio:
    def __init__(self, UPB):
        from collections import deque
        self.wavgCDR = 10
        self.wavgCoupon = 20
        self.wavgCPR = 15
        self.wavgRemTerm = 60
        self.loanUPB = UPB
        self.principalPayments = 0
        self.realizedLosses = 0
        self.interestIncome = 0
        self.loanYield = deque()

    def addLoans(self,newLoanUPB,newLoanCoupon,newLoanCDR,newRemTerm=60):
        self.wavgCDR = (self.loanUPB*self.wavgCDR + newLoanUPB*newLoanCDR)/(self.loanUPB + newLoanUPB)
        self.wavgCoupon = (self.loanUPB*self.wavgCoupon + newLoanUPB*newLoanCoupon)/(self.loanUPB + newLoanUPB)
        self.wavgRemTerm = (self.loanUPB*self.wavgRemTerm + newLoanUPB*newRemTerm)/(self.loanUPB + newLoanUPB)
        self.loanUPB += newLoanUPB

    def sellLoans(self,soldLoanUPB,soldLoanCoupon,soldLoanCDR):
        self.wavgCDR = (self.loanUPB*self.wavgCDR - soldLoanUPB*soldLoanCDR)/(self.loanUPB - soldLoanUPB)
        self.wavgCoupon = (self.loanUPB*self.wavgCoupon - soldLoanUPB*soldLoanCoupon)/(self.loanUPB - soldLoanUPB)
        self.loanUPB -= soldLoanUPB

    def runLoans(self,economy):
        if self.wavgRemTerm <=0.1:
            self.realizedLosses = 0
            self.principalPayments = self.loanUPB
            self.loanUPB = 0
            self.interestIncome = 0
            return

        self.realizedLosses = self.loanUPB * (self.wavgCDR + economy)/400
        self.loanUPB = self.loanUPB - self.realizedLosses
        self.interestIncome = self.loanUPB * self.wavgCoupon/400
        self.principalPayments = -np.ppmt(self.wavgCoupon/1200,60 - self.wavgRemTerm,60,self.loanUPB) - np.ppmt(self.wavgCoupon/1200,60 - self.wavgRemTerm - 1,60,self.loanUPB) - np.ppmt(self.wavgCoupon/1200,60 - self.wavgRemTerm - 2,60,self.loanUPB)
        self.principalPayments += self.loanUPB*self.wavgCPR/400

        if self.loanUPB >= 0.1:
            if len(self.loanYield) <= 3:
                self.loanYield.append((self.interestIncome - self.realizedLosses)/self.loanUPB)
            else:
                self.loanYield.popleft()
                self.loanYield.append((self.interestIncome - self.realizedLosses)/self.loanUPB)

        self.wavgRemTerm -= 3
        self.loanUPB = self.loanUPB - self.principalPayments



class Buyer:
    def __init__(self):
        self.cash = 3000
        self.confidence = 0
        self.happiness = 5
        self.purchased = False
        self.portfolio = Portfolio(0)

    def checkEmotions(self):
        if not self.purchased:
            self.confidence = max(0,self.confidence-0.1)

        if self.portfolio.loanUPB < 50:
            pass
        elif (self.portfolio.interestIncome - self.portfolio.realizedLosses) / self.portfolio.loanUPB * 4 > 0.1:
            self.happiness = min(10,self.happiness+0.2)
        else:
            self.happiness = max(0,self.happiness-0.2)

        self.cash += self.portfolio.interestIncome + self.portfolio.principalPayments



class TrancheBuyer:
    def __init__(self):
        self.cash = 3000
        self.purchased = False
        self.assets = []
        self.confidence = 0

    def updateHoldings(self):
        for asset in self.assets:
            self.cash += asset.prinPay
            self.cash += asset.intPay


class Company:
    def __init__(self,f):

        #Income Statement
        self.interestIncome = 0
        self.originationFees = 0 #Noninterest Income
        self.servicingFees = 0

        self.reserveChange = 0

        self.residualGain = 0 #Income statement equity method?

        self.facilityIncome = 0

        self.SGA = 50
        self.corporateOverhead = 150

        self.netIncome = 0


        #Loan Information
        self.portfolio = Portfolio(1000)
        self.wavgCDR = 10
        self.wavgCoupon = 20
        self.wavgCPR = 15
        self.wavgRemTerm = 60

        #Servicing Info
        self.soldPortfolioA = Portfolio(0)
        self.soldPortfolioB = Portfolio(0)
        self.securitizedLoanUPB = 0


        #Balance Sheet
        self.priorCash = 9000
        self.cash = 9000
        self.loanUPB = self.portfolio.loanUPB
        self.lossReserve = 100

        self.facility = f

        self.equity = 9900
        self.residualInvestments = 0 #Par value of all residuals
        self.residList = [] #List of all structures
        self.shares = 1000
        self.percentOwnership = 100


        #Cash Flow Statement
        self.originations = 200
        self.residualPayments = 0
        self.loanSales = 0
        self.securitizedPrincipal = 0
        self.equitySales = 0
        self.facilityCF = 0

        self.burnRate = 400
        self.runway = 9000/400

        #Player Decisions
        self.goodUW = 2
        self.UW = 1
        self.badUW = 1

        self.expectedCashBurn = 0

        self.quarter = 1
        self.year = 2018


    def originateLoans(self,economy):

        goodUPB = 50*((economy-0.5)*2/10+1)*self.goodUW
        okUPB = 50*self.UW
        badUPB = 50*((0.5-economy)*2/10+1)*self.badUW
        newLoanUPB = goodUPB + okUPB + badUPB

        newLoanCDR = (4*goodUPB + 6.5*okUPB + 9*badUPB)/newLoanUPB

        self.originations = newLoanUPB
        newLoanCoupon = 21 #<----------------Remember to add something cooler here

        self.portfolio.addLoans(newLoanUPB,newLoanCoupon,newLoanCDR)

        self.cash -= newLoanUPB*0.97
        self.originationFees = newLoanUPB * 0.03


    def addUnderwriters(self,num):
        from random import randint

        if num < 0:
            while self.badUW > 0 and num < 0:
                self.badUW -= 1
                num += 1
                self.SGA -= 4
            while self.UW > 0 and num < 0:
                self.UW -= 1
                num += 1
                self.SGA -= 4
            while self.goodUW > 0 and num < 0:
                self.goodUW -= 1
                num += 1
                self.SGA -= 4
        else:
            #Make this vary depending on number hired. More hired -> worse outcomes
            for i in range(num):
                x = randint(0,9)
                if x < 3:
                    self.badUW += 1
                    self.SGA += 4
                elif x < 6:
                    self.UW += 1
                    self.SGA += 4
                else:
                    self.goodUW += 1
                    self.SGA += 4



    def runResids(self,economy):
        self.residualInvestments = 0
        self.residualGain = 0
        self.residualPayments = 0
        self.securitizedLoanUPB = 0

        for structure in self.residList:
            priorBal = structure.bal
            structure.step(economy)
            self.residualPayments += structure.cf
            self.residualInvestments += structure.bal
            self.securitizedLoanUPB += structure.collatBal
            self.residualGain += (structure.bal + structure.cf - priorBal)


    def updateIncomeStatement(self,economy):

        self.portfolio.runLoans(economy)

        #Calculate Loss Reserve Changes
        self.lossReserve -= self.portfolio.realizedLosses
        oldReserve = self.lossReserve
        self.lossReserve = self.portfolio.loanUPB * self.portfolio.wavgCDR/100
        self.reserveChange = oldReserve - self.lossReserve

        #Calculate servicing fees
        self.servicingFees = (self.portfolio.loanUPB + self.securitizedLoanUPB + self.soldPortfolioA.loanUPB + self.soldPortfolioB.loanUPB) * 0.01/4

        self.netIncome = self.portfolio.interestIncome + self.originationFees + self.servicingFees + self.residualGain + self.reserveChange - self.corporateOverhead - self.SGA


    def updateCashFlowStatement(self):
        self.cash = self.cash + self.equitySales + self.portfolio.principalPayments + self.residualPayments + self.interestIncome + self.servicingFees - self.corporateOverhead - self.SGA
        self.burnRate = self.priorCash - self.cash
        self.runway = self.cash / self.burnRate
        self.priorCash = self.cash


    def updateBalanceSheet(self):
        self.equity += self.netIncome
        self.loanUPB = self.portfolio.loanUPB


class Facility:
    def __init__(self,maxSize=2000,intRate=0.08,advanceRate=0.9):
        self.maxSize = maxSize
        self.intRate = intRate
        self.advanceRate = advanceRate
        self.portfolio = Portfolio(0)
        self.loanSize = 0
        self.accrued = 0
        self.div = 0

    def updateFacility(self,c,economy):
        self.portfolio.runLoans(economy)
        self.accrued += (self.loanSize * self.intRate/4)
        cf = self.portfolio.interestIncome + self.portfolio.principalPayments

        if cf > self.accrued:
            cf -= self.accrued
            self.accrued = 0
        else:
            self.accrued -= cf
            cf = 0

        desiredLoan = self.portfolio.loanUPB * self.advanceRate
        if cf <= self.loanSize - desiredLoan:
            self.loanSize -= cf
            cf = 0
        else:
            cf -= (self.loanSize - desiredLoan)
            self.loanSize = desiredLoan

        self.div = cf
        c.cash += cf




class Structure:
    def __init__(self,tranches,portfolio,overcollat):
        self.portfolio = portfolio
        self.intPay = 0
        self.prinPay = 0
        self.cf = 0
        self.totalcf = 0
        self.collatBal = self.portfolio.loanUPB
        self.default = 0

        self.noteBal = 0
        self.intReq = 0
        for tranche in tranches:
            tranche.structure = self
            self.noteBal += tranche.bal
            self.intReq += tranche.bal*tranche.rate/12

        self.bal = self.collatBal - self.noteBal
        self.tranches = tranches
        self.overcollat = overcollat
        self.cfHist = []

    def step(self,economy):
        self.collatBal = 0
        self.totalcf = 0

        if self.portfolio.loanUPB == 0:
            for tranche in self.tranches:
                tranche.prinPay = 0
                tranche.intPay = 0
            self.intPay = 0
            return

        self.portfolio.runLoans(economy)
        self.totalcf += self.portfolio.interestIncome + self.portfolio.principalPayments
        self.collatBal = self.portfolio.loanUPB
        calcNoteBal = self.collatBal*self.overcollat
        remainingCF = self.totalcf
        reqPrinPay = self.noteBal - calcNoteBal

        for tranche in self.tranches:
            if remainingCF > tranche.bal*tranche.rate/4:
                tranche.intPay = tranche.bal*tranche.rate/4
                remainingCF -= tranche.intPay
            else:
                tranche.intPay = remainingCF
                remainingCF = 0
        if remainingCF > 0:
            for tranche in self.tranches:
                if reqPrinPay > tranche.bal:
                    if remainingCF > tranche.bal:
                        tranche.prinPay = tranche.bal
                        remainingCF -= tranche.bal
                        reqPrinPay -= tranche.bal
                        tranche.bal = 0
                    else:
                        tranche.prinPay = remainingCF
                        remainingCF = 0
                        tranche.bal -= remainingCF
                        break
                else:
                    if remainingCF > reqPrinPay:
                        tranche.prinPay = reqPrinPay
                        remainingCF -= reqPrinPay
                        tranche.bal -= reqPrinPay
                        reqPrinPay = 0
                    else:
                        tranche.prinPay = remainingCF
                        tranche.bal -= remainingCF
                        remainingCF = 0

        self.intPay = remainingCF
        self.cf = remainingCF
        self.cfHist.append(remainingCF)
        self.noteBal = 0
        self.intReq = 0
        for tranche in self.tranches:
            self.noteBal += tranche.bal
            self.intReq += tranche.bal*tranche.rate/4

        self.bal = self.collatBal - self.noteBal

    #Currently unused based on older version of project
    def simIRR(self,mark,CDR=0,CPR=0):
        from copy import deepcopy
        simStructure = Structure(deepcopy(self.tranches),deepcopy(self.collatList),deepcopy(self.overcollat),self.stepNum)
        markCF = [-mark]
        while simStructure.collatBal > 0:
            simStructure.step()
            markCF.append(simStructure.cf)
        monthlyReturn = np.irr(markCF)
        APR = (1+monthlyReturn)**12-1
        return APR

    #Currently unused based on older version of project
    def simMark(self,discount,CDR=0,CPR=0):
        from copy import deepcopy
        simStructure = Structure(deepcopy(self.tranches),deepcopy(self.collatList),deepcopy(self.overcollat),self.stepNum)
        while simStructure.collatBal > 0:
            simStructure.step()
        return np.npv(discount/12,simStructure.cfHist)


class Tranche:
    def __init__(self,bal,rate):
        self.bal = bal
        self.rate = rate
        self.intPay = 0
        self.prinPay = 0
        self.tranche = None