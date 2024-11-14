#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:10:18 2021

@author: sxu
"""
import numpy as np
import json as js
import datetime as dt
import os.path
from time import sleep
import sys

import matplotlib.pyplot as plt

def find_path():
    home_dir = os.path.expanduser("~")  # Get the home directory
    for root, dirs, files in os.walk(home_dir):  # Walk through the directory structure
        if 'cookstock' in dirs:
            return os.path.join(root, 'cookstock')
    return None  # Return None if the folder was not found
basePath = find_path()
yhPath = os.path.join(basePath, 'yahoofinancials')
sys.path.insert(0, yhPath)
from yahoofinancials import YahooFinancials

#define some constants
class algoParas:   
    PIVOT_PRICE_PERC = 0.2
    VOLUME_DROP_THRESHOLD_HIGH = 0.8
    VOLUME_DROP_THRESHOLD_LOW = 0.4
    REGRESSION_DAYS = 100
    PEAK_VOL_RATIO = 1.3
    PRICE_POSITION_LOW = 0.66
    
    

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
    m_recordVCP = []
    m_footPrint = []
    current_stickerPrice = []
    #define some parameters
    
    def __init__(self, ticker):
        super().__init__(ticker)  # Calls the parent class's initializer
        if isinstance(ticker, str):
            self.ticker = ticker.upper()
        else:
            self.ticker = [t.upper() for t in ticker]
        self._cache = {}
        date = dt.date.today()
        self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        self.current_stickerPrice = self.get_current_price()
        
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
            #check if the key is in the dictionary
            if not(self.bshData[self.ticker][i][date_key].get('stockholdersEquity')):
                #warning
                print('stockholdersEquity is not in the dictionary')
                break
            bv.append(self.bshData[self.ticker][i][date_key]['stockholdersEquity'])
        return bv
    
    def get_BV_quarter(self, numofQuarter=20):
        bv = []
        if not(self.bshData_quarter):
            self.get_balanceSheetHistory_quarter()
        for i in range(min(np.size(self.bshData_quarter[self.ticker]), numofQuarter)):
            date_key = list(self.bshData_quarter[self.ticker][i].keys())[0]
            if not(self.bshData_quarter[self.ticker][i][date_key]):    
                break
            if not(self.bshData_quarter[self.ticker][i][date_key].get('stockholdersEquity')):
                #warning
                print('stockholdersEquity is not in the dictionary')
                break
            bv.append(self.bshData_quarter[self.ticker][i][date_key]['stockholdersEquity'])
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
            #check if the key is in the dictionary
            if not(self.bshData[self.ticker][i][date_key].get('stockholdersEquity')):
                #warning
                print('stockholdersEquity is not in the dictionary')
                break
            equity = self.bshData[self.ticker][i][date_key]['stockholdersEquity']
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
            #check if the key is in the dictionary
            if not(self.cfsh[self.ticker][i][date_key].get('operatingCashFlow')):
                #warning
                print('operatingCashFlow is not in the dictionary')
                break
            totalCash.append(self.cfsh[self.ticker][i][date_key]['operatingCashFlow'])  
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
        # Filter out None values from bv
        bv_filtered = [value for value in bv if value is not None]
        
        gr = []
        for v in range(np.size(bv_filtered) - 1):
            # Calculate growth rate between consecutive years
            gr.append((bv_filtered[v] - bv_filtered[v + 1]) / abs(bv_filtered[v + 1]))

        return np.size(bv_filtered) - 1, np.median(gr) if gr else None
    
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
    def get_ma_ref(self, date_from, date_to):
        data = self.get_historical_price_data(str(date_from),str(date_to), 'daily')
        tmp = 0
        if not(data[self.ticker]['prices']):
            return -1
        for i in range(len(data[self.ticker]['prices'])):
            #print(data[self.ticker]['prices'][i]['formatted_date'])
            if not(data[self.ticker]['prices'][i]['close']):
                data[self.ticker]['prices'][i]['close'] = data[self.ticker]['prices'][i-1]['close']
            tmp = tmp + data[self.ticker]['prices'][i]['close']
        return tmp/(i+1)
    
    def get_ma(self, date_from, date_to):
        if not(self.priceData):
            date = dt.date.today()
            self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        #don't need to pull data from remote, use local
        priceDataStruct = self.priceData[self.ticker]['prices']
        selectedPriceDataStruct = self.get_price_from_buffer_start_end(priceDataStruct, date_from, date_to)
        #data = self.get_historical_price_data(date_from,date_to, 'daily')
        tmp = 0
        if not(selectedPriceDataStruct):
            return -1
        for i in range(len(selectedPriceDataStruct)):
            #print(data[self.ticker]['prices'][i]['formatted_date'])
            if not(selectedPriceDataStruct[i]['close']):
                selectedPriceDataStruct[i]['close'] = selectedPriceDataStruct[i-1]['close']
            tmp = tmp + selectedPriceDataStruct[i]['close']
        return tmp/(i+1)
    
    def get_ma_50(self, date):
        date_from = (date - dt.timedelta(days=50))
        date_to = (date)
        return self.get_ma(date_from, date_to)
    def get_ma_200(self, date):
        date_from = (date - dt.timedelta(days=200))
        date_to = (date)
        return self.get_ma(date_from, date_to)
    def get_ma_150(self, date):
        date_from = (date - dt.timedelta(days=150))
        date_to = (date)
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
        return -1
    
    def mv_strategy(self):
        if not(self.priceData):
            date = dt.date.today()
            self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        if not self.current_stickerPrice:
            self.current_stickerPrice = self.get_current_price()
        currentPrice = self.current_stickerPrice
        price50 = self.get_ma_50(dt.date.today())
        price150 = self.get_ma_150(dt.date.today())
        price200 = self.get_ma_200(dt.date.today())
        #print(currentPrice, price50, price150, price200, self.get_30day_trend_ma200())
        if currentPrice > price200 and self.get_30day_trend_ma200() == 1:
            return 1
        return -1  
        
    def get_vol(self, checkDays, avrgDays):
        date = dt.date.today()
        vol3day = []
        vol50day = []
        if not self.priceData:
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
        # Fetch the 3-day and 50-day volume averages
        vol3day, avgVol3day, vol50day, avgVol50day = self.get_vol(3, 200)

        # Check if 3-day average volume is at least 1.5x the 50-day average volume
        if avgVol3day >= algoParas.PEAK_VOL_RATIO* avgVol50day:
            return 1  # Volume condition met based on recent surge
        
        # # Check if 50-day average volume is above a minimum threshold (e.g., 800,000 shares)
        # if avgVol50day >= 800000:
        #     print("Consistent trading interest with 50-day average volume above 800,000 shares.")
        #     return 1  # Volume condition met based on sustained interest

        # If neither condition is met, the strategy fails
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
        if not self.current_stickerPrice:
            self.current_stickerPrice = self.get_current_price()
        currentPrice = self.current_stickerPrice
        highestPrice = np.max(closePrice)
    # Calculate range position as a percentage
        range_position = (currentPrice - lowestPrice) / (highestPrice - lowestPrice)

        # Conditions: within the upper third but below 90% of the 1-year high
        if algoParas.PRICE_POSITION_LOW <= range_position: #if it is larger than 1, it means it break out
            return 1  # Passes price positioning criteria
        return -1  # Fails price strategy
        
    def get_price_from_buffer(self, priceDataStruct, startDate, frame):
        selectedPriceDataStruct = []
        ##for each date
        currentDate = dt.date.today()
        dateList = []
        i = 0
        while(True):
            dateList.append(startDate + dt.timedelta(i))
            i = i + 1
            if dateList[-1] == currentDate:
                break
        for dd in dateList:
            for item in priceDataStruct:
                if item['formatted_date'] == str(dd):
                    selectedPriceDataStruct.append(item)
                    frame = frame - 1
                if frame <= 0:
                    break
        return selectedPriceDataStruct
    
    def get_price_from_buffer_start_end(self, priceDataStruct, startDate, endDate):
        selectedPriceDataStruct = []
        ##for each date
        currentDate = dt.date.today()
        dateList = []
        i = 0
        while(True):
            dateList.append(startDate + dt.timedelta(i))
            i = i + 1
            if dateList[-1] == endDate:
                break
        for dd in dateList:
            for item in priceDataStruct:
                if item['formatted_date'] == str(dd):
                    selectedPriceDataStruct.append(item)
        return selectedPriceDataStruct
        
#given start date and a time frame, if no price on that day, just move to next day
    def get_price(self, startDate, frame):
        to_date = startDate + dt.timedelta(frame)
        if not(self.priceData):
            date = dt.date.today()
            self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        #don't need to pull data from remote, use local
        priceDataStruct = self.priceData[self.ticker]['prices']
        selectedPriceDataStruct = self.get_price_from_buffer(priceDataStruct, startDate, frame)
        
                
        return selectedPriceDataStruct
    
    def get_price_ref(self, startDate, frame):
        to_date = startDate + dt.timedelta(frame)
        if not(self.priceData):
            date = dt.date.today()
            self.priceData = self.get_historical_price_data(str(date -  dt.timedelta(days=365)), str(date), 'daily')
        #don't need to pull data from remote, use local
        priceData = self.get_historical_price_data(str(startDate), str(to_date), 'daily')
        priceDataStruct = priceData[self.ticker]['prices']    
        return priceDataStruct
    
    def get_highest_in5days(self, startDate):
        priceData = []
        priceDataStruct = self.get_price(startDate, 5)
        tmpLen = len(priceDataStruct)
        for i in range(tmpLen):
            priceData.append(priceDataStruct[i]['close'])
        if not(priceData):
            return [-1, -1]
        else:
            highestPrice = np.max(priceData)
            ind = np.argmax(priceData)
        return highestPrice, priceDataStruct[ind]['formatted_date']
    
    def get_lowest_in5days(self, startDate):
        priceData = []
        priceDataStruct = self.get_price(startDate, 5)
        tmpLen = len(priceDataStruct)
        for i in range(tmpLen):
            priceData.append(priceDataStruct[i]['close'])
        if not(priceData):
            return [-1, -1]
        else:
            lowestPrice = np.min(priceData)
            ind = np.argmin(priceData)
        return lowestPrice, priceDataStruct[ind]['formatted_date']
        
    def find_one_contraction(self, startDate):
        print('start searching date')
        print(startDate)
        date = dt.date.today()
        tmp = date - startDate
        numOfDate = tmp.days
        localHighestPrice = -100000
        localHighestDate = -1
        counter = 0
        counterThr = 5
        flag = True
        for i in range(numOfDate):
            movingDate = startDate + dt.timedelta(i)
            #print(movingDate)
            price, priceDate = self.get_highest_in5days(movingDate)
            if price == -1 and priceDate == -1:
                flag = False
                return flag, -1, -1, -1, -1
            if price > localHighestPrice:
                localHighestPrice = price
                localHighestDate = priceDate
                counter = 0
            else:
                counter = counter + 1
                print('start lock the date')
                print(priceDate)
            if counter >= counterThr:
                #get local high
                print('find the local highest price')
                print(localHighestPrice)
                print('date is')
                print(localHighestDate)
                break
        if counter < counterThr:
            flag = False
            return flag, -1, -1, -1, -1
            
        #search for local low
        if counter >= counterThr:
            print('start search for lowest price')
            tmp_dt = dt.datetime.strptime(localHighestDate, "%Y-%m-%d")
            localHighestDate_dt = tmp_dt.date()
            tmp = date - localHighestDate_dt
            numOfDate2 = tmp.days
            startDate2 = localHighestDate_dt
            localLowestPrice = 1000000
            localLowestDate = -1
            counter2 = 0
            for j in range(numOfDate2):
                movingDate2 = startDate2 + dt.timedelta(j)
                price, priceDate = self.get_lowest_in5days(movingDate2)
                if price == -1 and priceDate == -1:
                    break
                if price < localLowestPrice:
                    localLowestPrice = price
                    localLowestDate = priceDate
                    counter2 = 0
                else:
                    counter2 = counter2 + 1
                    print('start lock the date')
                    print(priceDate)
                if counter2 >= counterThr:
                    #get local high
                    print('find the local lowest price')
                    print(localLowestPrice)
                    print('date is')
                    print(localLowestDate)
                    break
                
        #
        if localHighestPrice == localLowestPrice:
            return False, -1, -1, -1, -1
        return flag, localHighestDate, localHighestPrice, localLowestDate, localLowestPrice
                
    def find_volatility_contraction_pattern(self, startDate):
        recordVCP = []
        self.m_recordVCP = []
        counterForVCP = 0
        flagForOneContraction, hD, hP, lD, lP = self.find_one_contraction(startDate)
        if flagForOneContraction == True:
            recordVCP.append([hD, hP, lD, lP])
        else:
            print('not find any contraction pattern')
            return counterForVCP, []
        while(True):
            counterForVCP = counterForVCP + 1
            lD_tmp = dt.datetime.strptime(lD, "%Y-%m-%d")
            startDate = lD_tmp.date()
            flagForOneContraction, hD, hP, lD, lP = self.find_one_contraction(startDate)
            if flagForOneContraction == False:
                break
            recordVCP.append([hD, hP, lD, lP])
        if counterForVCP == 1:
            self.m_recordVCP = recordVCP
            return counterForVCP, self.m_recordVCP
        ind = 0    
        icounter = 0
        
        while(True):
            if ind >= counterForVCP:
                return icounter, self.m_recordVCP
            currentHightDate = recordVCP[ind][0]
            currentHightPrice = recordVCP[ind][1]
            currentLowDate = recordVCP[ind][2]
            currentLowPrice = recordVCP[ind][3]
            lastHP = currentHightPrice
            lastLP = currentLowPrice
            
            if ind+1 >= counterForVCP:
                self.m_recordVCP.append([currentHightDate, currentHightPrice, currentLowDate, currentLowPrice])
                icounter = icounter + 1
                return icounter, self.m_recordVCP
            
            
            for i in range(ind+1, counterForVCP):
                if recordVCP[i][1] < lastHP and recordVCP[i][3] < lastLP:
                    lastHP = recordVCP[i][1]
                    lastLP = recordVCP[i][3]
                    currentLowPrice = recordVCP[i][3]
                    currentLowDate = recordVCP[i][2]
                    ind = i + 1
                else:
                    ind = i
                    break
            self.m_recordVCP.append([currentHightDate, currentHightPrice, currentLowDate, currentLowPrice])
            icounter = icounter + 1
            
    
    def get_footPrint(self):
        flag = False
        if not(self.m_recordVCP):
            date_from = (dt.date.today() - dt.timedelta(days=60))
            self.find_volatility_contraction_pattern(date_from)
        length = len(self.m_recordVCP)
        self.m_footPrint=[]
        for i in range(length):            
            self.m_footPrint.append([self.m_recordVCP[i][0], self.m_recordVCP[i][2], (self.m_recordVCP[i][1]-self.m_recordVCP[i][3])/self.m_recordVCP[i][1]])
        return self.m_footPrint
    
    def is_pivot_good(self):
        flag = False
        if not(self.m_footPrint):
            self.get_footPrint()
        #correction within 10% of max price and current price higher then lower boundary
        if not self.current_stickerPrice:
            current = self.get_current_price()
        else:
            current = self.current_stickerPrice
        flag = (self.m_footPrint[-1][2] <= algoParas.PIVOT_PRICE_PERC) and (current> self.m_recordVCP[-1][3])
        #report support and pressure
        print(self.ticker + ' current price: ' + str(current))
        print(self.ticker + ' support price: ' + str(self.m_recordVCP[-1][3]))
        print(self.ticker + ' pressure price: ' + str(self.m_recordVCP[-1][1]))
        return flag, current, self.m_recordVCP[-1][3], self.m_recordVCP[-1][1]
    
    def is_correction_deep(self):
        flag = False
        if not(self.m_footPrint):
            self.get_footPrint()
        tmp = np.asarray(self.m_footPrint)
        tmpcorrection = tmp[:,2]
        correction = tmpcorrection.astype(float)
        return correction.max() >= 0.5
    #check the last contraction, is the demand dry

    def is_demand_dry(self):
        if not self.m_footPrint:
            self.get_footPrint()

        # Get the date range from the last footprint entry
        startDate = self.m_footPrint[-1][0]
        endDate = self.m_footPrint[-1][1]
        startDate_dt = dt.datetime.strptime(startDate, "%Y-%m-%d")
        endDate_dt = dt.datetime.strptime(endDate, "%Y-%m-%d")

        # Load price data if not already loaded
        if not self.priceData:
            date = dt.date.today()
            self.priceData = self.get_historical_price_data(str(date - dt.timedelta(days=365)), str(date), 'daily')

        # Fetch volumes for the specific period in the footprint
        priceDataStruct = self.priceData[self.ticker]['prices']
        footprintVolume = self._extract_volume_for_period(priceDataStruct, startDate_dt.date(), endDate_dt.date())

        # Calculate the volume trend using linear regression
        slope, intercept = self._calculate_volume_trend(footprintVolume)
        
        #get past 4 days volume
        recentData = priceDataStruct[-4:]
        recentStartDate = recentData[0]['formatted_date']
        recentEndDate = recentData[-1]['formatted_date']
        recentVolume = [item['volume'] for item in recentData]
        slopeRecent, interceptRecent = self._calculate_volume_trend(recentVolume)

        # Determine if demand is dry based on slope and volume comparison
        isDry = (slope <= 0) or (slopeRecent <= 0)
        return isDry, startDate, endDate, footprintVolume, slope, intercept, recentStartDate, recentEndDate, recentVolume, slopeRecent, interceptRecent

    def _extract_volume_for_period(self, priceDataStruct, start_date, end_date):
        """Extracts volume data for a specified period from price data."""
        selected_data = self.get_price_from_buffer_start_end(priceDataStruct, start_date, end_date)
        return [item['volume'] for item in selected_data]

    def _calculate_volume_trend(self, volume_list):
        """Performs linear regression to determine volume trend."""
        x = np.arange(len(volume_list))
        y = np.array(volume_list)
        slope, intercept = np.polyfit(x, y, 1)
        return slope, intercept

    def _calculate_historical_average_volume(self, priceDataStruct, days):
        """Calculates the average volume over the last 'days' period."""
        end_date = dt.date.today()
        start_date = end_date - dt.timedelta(days=days)
        historical_data = self.get_price_from_buffer_start_end(priceDataStruct, start_date, end_date)
        volume_list = [item['volume'] for item in historical_data]
        return np.mean(volume_list) if volume_list else 0
    
    
    def combined_best_strategy(self):
        # Check moving average strategy
        s = True
        if self.mv_strategy() != 1:
            s = s and False
        
        # Check volume strategy
        if self.vol_strategy() != 1:
            s = s and False
        
        # Check price strategy
        if self.price_strategy() != 1:
            s = s and False
        
        # Check if the stock is near a good pivot point
        isGoodPivot, currentPrice, supportPrice, resistancePrice = self.is_pivot_good()
        if not isGoodPivot:
            s = s and False
        
        # Check if recent correction is not too deep
        if self.is_correction_deep():
            s = s and False
        
        # Check if demand is drying up (selling pressure has decreased)
        isDemandDry, startDate, endDate, volume_ls, slope, intercept, _, _, _, _, _ = self.is_demand_dry()
        if not isDemandDry:
            s = s and False
        
        # All criteria met, return True for a strong buy signal
        return s



class batch_process:
    tickers = []
    resultsPath = ''
    result_file = ''
    
    def __init__(self, tickers, sessions):
        self.tickers = tickers
        basePath = find_path()
        current_date = dt.date.today().strftime('%Y-%m-%d')
        self.resultsPath = os.path.join(basePath, 'results', current_date)
        file = sessions + '.json'
        self.result_file = setup_result_file(self.resultsPath, file)
            
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
                if x.vol_strategy() == 1: #not from original book, not working
                    s2 = 1
                    print("passing 3 day volume strategy")
                if x.price_strategy() == 1:
                    s3 = 1
                    print("passing price strategy")
                #if s1==1 and s2==1 and s3==1:
                if s1==1 and s3==1 and s2:
                    print("congrats, this stock passes all strategys, run volatility contraction pattern")
                    superStock.append(self.tickers[i])    
                append_to_json(self.result_file, self.tickers[i])
            except Exception:
                print("error!")
                pass
        
            
    def batch_pipeline_full(self):
        superStock=[]
        date_from = (dt.date.today() - dt.timedelta(days=100))
        date_to = (dt.date.today())
        for i in range(np.size(self.tickers)):
            try:
                ticker = self.tickers[i]
                print(ticker)
                x = cookFinancials(ticker)
                flag = x.combined_best_strategy()
                if flag == True:
                    print("congrats, this stock passes all strategys")
                    superStock.append(ticker)
                    sp = x.get_price(date_from, 100)
                    tmpLen = len(sp)
                    date = []
                    price = []
                    volume = []
                    for i in range(tmpLen):
                        date.append(sp[i]['formatted_date'])
                        price.append(sp[i]['close'])
                        volume.append(sp[i]['volume'])
                    # create figure and axis objects with subplots()
                    fig,ax = plt.subplots(2)
                    fig.suptitle(x.ticker)
                    # make a plot
                    ax[0].plot(date, price, color="blue", marker="o")
                    # set x-axis label
                    ax[0].set_xlabel("date",fontsize=14)
                    # set y-axis label
                    ax[0].set_ylabel("stock price",color="blue",fontsize=14)
                    
                    # twin object for two different y-axis on the sample plot
                    # make a plot with different y-axis using second axis object
                    ax[1].bar(date, np.asarray(volume)/10**6 ,color="green")
                    ax[1].set_ylabel("volume (m)",color="green",fontsize=14)
                    #ax[1].set_ylim([0, 100])
                    
                    # Set x-ticks to display every 10th date and include the last date
                    xticks = np.arange(0, len(date), 10).tolist()
                    if len(date) - 1 not in xticks:  # Check if the last date is already included
                        xticks.append(len(date) - 1)  # Add the last date index to x-ticks

                    ax[0].set_xticks(xticks)
                    ax[1].set_xticks(xticks)

                    # Format date labels for readability
                    fig.autofmt_xdate(rotation=45)
                    
                    print(x.get_highest_in5days(date_from))
                    
                    counter, record = x.find_volatility_contraction_pattern(date_from)
                    
                    if counter > 0:
                        for i in range(counter):
                            ax[0].plot([record[i][0], record[i][2]], [record[i][1], record[i][3]], 'r')
                        
                        # ax[0].set_xticks(np.arange(0, len(date)+1, 12))
                        # ax[1].set_xticks(np.arange(0, len(date)+1, 12))
                        
                        print('footprint:')
                        footprint = x.get_footPrint()
                        print(footprint)
                        print('is a good pivot?')
                        isGoodPivot, currentPrice, supportPrice, pressurePrice = x.is_pivot_good()
                        print(isGoodPivot)
                        print('is a deep correction?')
                        isDeepCor = x.is_correction_deep()
                        print(isDeepCor)
                        print('is demand dried?')
                        isDemandDry, startDate, endDate, volume_ls, slope, interY, recentStart, recentEnd, volume_re, slopeRecet, interYRecent = x.is_demand_dry()
                        print(isDemandDry)
    
                        ticker_data = {ticker:{'current price':str(currentPrice), 'support price':str(supportPrice), 'pressure price':str(pressurePrice), \
                                    'is_good_pivot':str(isGoodPivot), 'is_deep_correction':str(isDeepCor), 'is_demand_dry': str(isDemandDry)}}    

                        for ind, item in enumerate(date):
                            if item == startDate:
                                print(ind)
                                break
                        x_axis = []
                        for i in range(len(volume_ls)):
                            x_axis.append(ind+i)
                        x_axis = np.array(x_axis)
                        
                        y = slope*x_axis-slope*ind + volume_ls[0]
                        ax[1].plot(np.asarray(date)[x_axis], y/10**6, color="red",linewidth=4)
                        
                        for ind, item in enumerate(date):
                            if item == recentStart:
                                print(ind)
                                break
                        x_axis = []
                        for i in range(len(volume_re)):
                            x_axis.append(ind+i)
                        x_axis = np.array(x_axis)
                        yRecent = slopeRecet*x_axis-slopeRecet*ind + volume_re[0]
                        ax[1].plot(np.asarray(date)[x_axis], yRecent/10**6, color="red",linewidth=4)
                        fig.show()
                        
                        figName = os.path.join(self.resultsPath, ticker+'.jpg')
                        #only save the ones passing all criterion
                        if isGoodPivot and not(isDeepCor) and isDemandDry:
                            fig.savefig(figName,
                                        format='jpeg',
                                        dpi=100,
                                        bbox_inches='tight')
                            #add link to the json file
                            ticker_data[ticker]['fig'] = figName
                            
                        append_to_json(self.result_file, ticker_data)
            except Exception:
                print("error!")
                pass

            
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
                stickerPrice = x.current_stickerPrice
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
                        "stock price":stickerPrice,                     
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
            
def load_json(filepath):
    with open(filepath, "r") as f:
        return js.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        js.dump(data, f, indent=4)

def append_to_json(filepath, ticker_data):
    data = load_json(filepath)
    data['data'].append(ticker_data)
    save_json(filepath, data)

def setup_result_file(basePath, file):
    # check if each level directory exists
    if not os.path.exists(basePath):
        os.makedirs(basePath)
    filepath = os.path.join(basePath, file)
    save_json(filepath, {"data": []})
    return filepath