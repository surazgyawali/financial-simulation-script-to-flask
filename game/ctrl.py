#!/venv/bin/python3

from random import randint
import numpy as np

from flask import Flask, flash, redirect, session, url_for, render_template, request

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