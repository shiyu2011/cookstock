#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:10:18 2021

@author: sxu
"""
from yahoofinancials import YahooFinancials
import numpy as np
import json as js
import datetime as dt
import os.path

class cookFinancials(YahooFinancials):
    ticker = ''
    bshData = []
    bshData_quarter = []
    ish = []
    ish_quarter = []
    cfsh = []
    cfsh_quarter = []
    summaryData = []
    priceData = []
    def __init__(self, ticker):
        if isinstance(ticker, str):
            self.ticker = ticker.upper()
        else:
            self.ticker = [t.upper() for t in ticker]
        self._cache = {}
        
    def get_balanceSheetHistory(self):
        self.bshData = self.get_financial_stmts('annual', 'balance')['balanceSheetHistory']
        return self.bshData
    
    def get_balanceSheetHistory_quarter(self):
        self.bshData_quarter = self.get_financial_stmts('quarterly', 'balance')['balanceSheetHistoryQuarterly']
        return self.bshData_quarter
    
    def get_incomeStatementHistory(self):
        self.ish = self.get_financial_stmts('annual', 'income')['incomeStatementHistory']
        return self.ish
    
    def get_incomeStatementHistory_quarter(self):
        self.ish_quarter = self.get_financial_stmts('quarterly', 'income')['incomeStatementHistoryQuarterly']
        return self.ish_quarter
    
    def get_cashflowStatementHistory(self):
        self.cfsh = self.get_financial_stmts('annual','cash')['cashflowStatementHistory']
        return self.cfsh
    def get_cashflowStatementHistory_quarter(self):
        self.cfsh_quarter = self.get_financial_stmts('quarterly','cash')['cashflowStatementHistoryQuarterly']
        return self.cfsh_quarter
    
    def get_BV(self, numofYears=20):
        bv = []
        if not(self.bshData):
            self.get_balanceSheetHistory()
        for i in range(min(np.size(self.bshData[self.ticker]), numofYears)):
            date_key = list(self.bshData[self.ticker][i].keys())[0]
            if not(self.bshData[self.ticker][i][date_key]):    
                break
            bv.append(self.bshData[self.ticker][i][date_key]['totalStockholderEquity'])
        return bv
    
    def get_BV_quarter(self, numofQuarter=20):
        bv = []
        if not(self.bshData_quarter):
            self.get_balanceSheetHistory_quarter()
        for i in range(min(np.size(self.bshData_quarter[self.ticker]), numofQuarter)):
            date_key = list(self.bshData_quarter[self.ticker][i].keys())[0]
            if not(self.bshData_quarter[self.ticker][i][date_key]):    
                break
            bv.append(self.bshData_quarter[self.ticker][i][date_key]['totalStockholderEquity'])
        return bv   
    
    def get_ROIC(self, numofYears=20):
        roic = []
        if not(self.cfsh):
            self.get_cashflowStatementHistory()
        if not(self.bshData):
            self.get_balanceSheetHistory()
        for i in range(min(np.size(self.bshData[self.ticker]), numofYears)):
            date_key = list(self.bshData[self.ticker][i].keys())[0]
            if not(self.bshData[self.ticker][i][date_key]):    
                break
            equity = self.bshData[self.ticker][i][date_key]['totalStockholderEquity']
            if self.bshData[self.ticker][i][date_key].get('shortLongTermDebt') is None or not(self.bshData[self.ticker][i][date_key]['shortLongTermDebt']):
                debt_short = 0
            else:
                debt_short = self.bshData[self.ticker][i][date_key].get('shortLongTermDebt')
            if self.bshData[self.ticker][i][date_key].get('longTermDebt') is None or not(self.bshData[self.ticker][i][date_key]['longTermDebt']) :
                debt_long = 0
            else:
                debt_long = self.bshData[self.ticker][i][date_key]['longTermDebt']
            debt = debt_short + debt_long
            date_key = list(self.cfsh[self.ticker][i].keys())[0]
            if not(self.cfsh[self.ticker][i][date_key]):    
                break
            netincome = self.cfsh[self.ticker][i][date_key]['netIncome']
            roic_year = netincome/(equity + debt)
            roic.append(roic_year)
        return roic 
    
    def get_totalCashFromOperatingActivities(self, numofYears=20):
        totalCash = []
        if not(self.cfsh):
            self.get_cashflowStatementHistory()        
        for i in range(min(np.size(self.cfsh[self.ticker]), numofYears)):
            date_key = list(self.cfsh[self.ticker][i].keys())[0]
            if not(self.cfsh[self.ticker][i][date_key]):    
                break
            totalCash.append(self.cfsh[self.ticker][i][date_key]['totalCashFromOperatingActivities'])  
        return totalCash
    
    def get_pricetoSales(self):
        if not(self.summaryData):
            self.summaryData = self.get_summary_data()
        if not(self.summaryData[self.ticker]):
            return 'na'
        return self.summaryData[self.ticker]['priceToSalesTrailing12Months']
    
    def get_marketCap_B(self):
        if not(self.summaryData):
            self.summaryData = self.get_summary_data()
        if not(self.summaryData[self.ticker]):
            return 'na'
        return self.summaryData[self.ticker]['marketCap']/1000000000
    
    def get_CF_GR_median(self, totalCash):
        gr = []
        for v in range(np.size(totalCash)-1):
            gr.append((totalCash[v]-totalCash[v+1])/abs(totalCash[v+1]))
        #print(gr)
        return np.size(totalCash)-1, np.median(gr) 
    
    #use mean of each year    
    def get_BV_GR_median(self, bv):
        gr = []
        for v in range(np.size(bv)-1):
            gr.append((bv[v]-bv[v+1])/abs(bv[v+1]))
        #print(gr)
        return np.size(bv)-1, np.median(gr)
    
    def get_GR_median(self, bv):
        gr = []
        for v in range(np.size(bv)-1):
            gr.append((bv[v]-bv[v+1])/abs(bv[v+1]))
        #print(gr)
        return np.size(bv)-1, np.median(gr)
    
    #use mean of each year    
    def get_ROIC_median(self, roic):
        return np.size(roic), np.median(roic)
    
    def get_BV_GR_max(self, bv):
        gr = []
        for v in range(np.size(bv)-1):
            gr.append((bv[v]-bv[v+1])/abs(bv[v+1]))
        #print(gr)
        return np.size(bv)-1, np.max(gr)
    
    def growthRate(self, cur,init, years):
        if cur <=0 or init<=0:
            return -1
        return (cur/init)**(1/years)-1
    
    def get_BV_GR_mean(self, bv):
        gr = []
        BV_GR = self.growthRate(bv[0], bv[np.size(bv)-1], np.size(bv)-1)
        if BV_GR==-1:
            for v in range(np.size(bv)-1):
                gr.append((bv[v]-bv[v+1])/abs(bv[v+1]))
            BV_GR = np.mean(gr)
        return np.size(bv)-1, BV_GR
    
    def get_suggest_price(self, cEPS, growth, years, rRate, PE, safty):
        if not(cEPS) or not(growth) or not(PE):
            return 'NA'
        fEPS = cEPS*(1+growth)**years
        fPrice = fEPS*PE;
        stickerPrice = fPrice/(1+rRate)**years
        return stickerPrice, stickerPrice*safty
    
    def payBackTime(self, price, cEPS, growth):
        tmp = 0
        i = 0
        if cEPS < 0:
            return 0
        while(growth>0):
            i+=1
            tmp = tmp + cEPS*(1+growth)**i
            if (tmp>price):
                break
        return i
    
    def get_earningsperShare(self):
        eps = self.get_earnings_per_share()
        if not(eps):
            eps = self.get_key_statistics_data()[self.ticker]['trailingEps']
        print(eps)
        return eps
    
    def get_PE(self):
        #print(self._stock_summary_data('trailingPE'))
        #print(self._stock_summary_data('forwardPE'))
        if not(self._stock_summary_data('trailingPE')):
            return self._stock_summary_data('forwardPE')
        if not(self._stock_summary_data('forwardPE')):
            return self._stock_summary_data('trailingPE')
        return (self._stock_summary_data('trailingPE')+self._stock_summary_data('forwardPE'))/2
    
    def get_decision(self,suggestPrice, stockprice):
        #print('suggested price:', suggestPrice)
        #print('stock price:', stockprice)
        if isinstance(suggestPrice, str):
            return 'skip due to negative eps'
        elif suggestPrice>stockprice:
            return 'strong buy' 
        else:
            return 'do not buy'   
    def get_ma(self, date_from, date_to):
        data = self.get_historical_price_data(date_from,date_to, 'daily')
        tmp = 0
        if not(data[self.ticker]['prices']):
            return -1
        for i in range(len(data[self.ticker]['prices'])):
            #print(data[self.ticker]['prices'][i]['formatted_date'])
            if not(data[self.ticker]['prices'][i]['close']):
                data[self.ticker]['prices'][i]['close'] = data[self.ticker]['prices'][i-1]['close']
            tmp = tmp + data[self.ticker]['prices'][i]['close']
        return tmp/(i+1)
    def get_ma_50(self, date):
        date_from = str(date - dt.timedelta(days=50))
        date_to = str(date)
        return self.get_ma(date_from, date_to)
    def get_ma_200(self, date):
        date_from = str(date - dt.timedelta(days=200))
        date_to = str(date)
        return self.get_ma(date_from, date_to)
    def get_ma_150(self, date):
        date_from = str(date - dt.timedelta(days=150))
        date_to = str(date)
        return self.get_ma(date_from, date_to)
    def get_30day_trend_ma200(self):
        ###no need to look at everyday, just check last, mid, current
        current = self.get_ma_200((dt.date.today()))
        #print(dt.date.today())
        #print(current)
        mid = self.get_ma_200((dt.date.today()-dt.timedelta(days=15)))
        #print(dt.date.today()-dt.timedelta(days=15))
        #print(mid)
        last = self.get_ma_200((dt.date.today()-dt.timedelta(days=30)))
        #print(dt.date.today()-dt.timedelta(days=30))
        #print(last)
        if current - mid > 0 and mid -last > 0:
            return 1
        else:
            return -1
    def mv_strategy(self):
        currentPrice = self.get_current_price()
        price50 = self.get_ma_50(dt.date.today())
        price150 = self.get_ma_150(dt.date.today())
        price200 = self.get_ma_200(dt.date.today())
        #print(currentPrice, price50, price150, price200, self.get_30day_trend_ma200())
        if currentPrice > price50 and currentPrice > price150 and currentPrice > price200 and price150 > price200 and price50 > price150 and price50 > price200 and self.get_30day_trend_ma200() == 1:
            return 1
        else:
            return -1  
        
    def get_vol(self, checkDays, avrgDays):
        date = dt.date.today()
        vol3day = []
        vol50day = []
        self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        length = len(self.priceData[self.ticker]['prices'])
        for i in range(checkDays):
            if not(self.priceData[self.ticker]['prices'][length-1-i]['volume']):
                self.priceData[self.ticker]['prices'][length-1-i]['volume'] = self.priceData[self.ticker]['prices'][length-1-i+1]['volume']
            vol3day.append(self.priceData[self.ticker]['prices'][length-1-i]['volume'])
        #print(vol3day)
        for i in range(np.min([avrgDays, length])):
            if not(self.priceData[self.ticker]['prices'][length-1-checkDays-i]['volume']):
                self.priceData[self.ticker]['prices'][length-1-checkDays-i]['volume'] = self.priceData[self.ticker]['prices'][length-1-checkDays-i+1]['volume']
        #    print(self.priceData[self.ticker]['prices'][length-1-checkDays-i]['volume'])
            vol50day.append(self.priceData[self.ticker]['prices'][length-1-checkDays-i]['volume'])
        return vol3day, np.sum(vol3day)/checkDays, vol50day, np.sum(vol50day)/avrgDays
    
    def vol_strategy(self):
        v3,a3,v50,a50 = self.get_vol(3, 50)
        if a3>a50*1.5 and np.max(a3) > 1000000: #1m trade
            return 1
        else:
            return -1
        
    def price_strategy(self):
        closePrice = []
        if not(self.priceData):
            date = dt.date.today()
            self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        length = len(self.priceData[self.ticker]['prices'])
        for i in range(length):
            if not(self.priceData[self.ticker]['prices'][i]['close']):
                self.priceData[self.ticker]['prices'][i]['close'] = self.priceData[self.ticker]['prices'][i-1]['close']
            closePrice.append(self.priceData[self.ticker]['prices'][i]['close'])
        lowestPrice = np.min(closePrice)
        currentPrice = self.get_current_price()
        highestPrice = np.max(closePrice)
        #print(currentPrice, lowestPrice, highestPrice)
        if currentPrice > lowestPrice*(1+0.3) and currentPrice > 0.75*highestPrice:
            return 1
        else:
            return -1
        
    def combine_strategy(self):
        if self.mv_strategy() and self.vol_strategy() and self.price_strategy():
            return self.ticker
        else:
            return -1
        
        
    def get_3day_vol(self):
        count = 0
        date = dt.date.today()
        vol = []
        while count < 3:
            print('request date: ',date)
            data = self.get_historical_price_data(str(date),str(date + dt.timedelta(days=1)), 'daily')
            if not(data[self.ticker]['prices']):
                date = date - dt.timedelta(days=1)
                continue
            else:
                print('response date: ', data[self.ticker]['prices'][0]['formatted_date'])
                vol.append(data[self.ticker]['prices'][0]['volume'])
                count = count + 1
                date = date - dt.timedelta(days=1)
        return vol, np.sum(vol)/3



class batch_process:
    def __init__(self, tickers, section):
        self.tickers = tickers
        self.jsfile = os.path.join('result', section)
        with open(self.jsfile, "w") as f:
            s = {"data":[]}
            js.dump(s, f, indent = 4)
            
    def batch_strategy(self):
        superStock=[]
        for i in range(np.size(self.tickers)):
            try:
                print(self.tickers[i])
                x = cookFinancials(self.tickers[i])
                s1=0
                s2=0
                s3=0
                if x.mv_strategy()==1:
                    s1 = 1
                    print("passing moving average strategy")
                if x.vol_strategy() == 1:
                    s2 = 1
                    print("passing 3 day volume strategy")
                if x.price_strategy() == 1:
                    s3 = 1
                    print("passing price strategy")
                if s1==1 and s2==1 and s3==1:
                    print("congrats, this stock passes all strategys, check yahoo finance to see how expert say")
                    superStock.append(self.tickers[i])                   
            except Exception:
                print("error!")
                pass
        s = tuple(superStock)
        print(s)
        with open(self.jsfile, "r") as f:
            data = js.load(f)
            cont = data['data']
            cont.append(s)
        with open(self.jsfile, "w") as f:
            js.dump(data, f, indent=4) 
            print('=====================================')
        
            
    def batch_financial(self):       
        for i in range(np.size(self.tickers)):
            try:
                print(self.tickers[i])
                x = cookFinancials(self.tickers[i])
                bv = x.get_BV(20)
                bv.insert(0, x.get_book_value())
                print(bv)
                bvgr = x.get_BV_GR_median(bv)
                print(bvgr)
                growth = bvgr[1]
                cEPS = x.get_earnings_per_share()
                print(cEPS)
                years = 3;
                rRate = 0.25;
                safty = 0.5
                PE = x.get_PE()
                price=x.get_suggest_price(cEPS, growth, years, rRate, PE, safty)
                print(price)
                stickerPrice = x.get_current_price()
                decision = x.get_decision(price[1],stickerPrice)
                print(decision)
                y2pb = 0
                roic = 0
                mcap = 0
                cashflow = 0
                priceSales = 0
                if decision == 'strong buy':
                    y2pb = x.payBackTime(stickerPrice, cEPS, growth)
                    roic = x.get_ROIC()
                    mcap = x.get_marketCap_B()
                    cashflow = (x.get_totalCashFromOperatingActivities())
                    priceSales = x.get_pricetoSales()               
                s = {
                    self.tickers[i]:{
                        "decision":decision,
                        "suggested price":price[1],
                        "stock price":x.get_current_price(),                     
                        "Payback years": y2pb,
                        "Book Value": bv,
                        "ROIC": roic,
                        "market cap (b)": mcap,
                        "cashflow": cashflow,
                        "priceSalesRatio":priceSales,
                        "PE": PE
                    }
                }
                print(s)
                with open(self.jsfile, "r") as f:
                    data = js.load(f)
                    cont = data['data']
                    cont.append(s)
                with open(self.jsfile, "w") as f:
                    js.dump(data, f, indent=4) 
                print('=====================================')
            except Exception:
                print("error!")
                pass
