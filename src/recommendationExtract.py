#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:49:51 2021

@author: sxu
"""
import numpy as np
import json as js
import datetime as dt
import requests
import pandas as pd 
from pandas_datareader import DataReader
import time

#ready json file to get ticker
with open('result/Tech_superStocks_2_5_2021.json') as f:
  data = js.load(f)
print(data)

tickers = data['data'][0]
recommendations = []
print(tickers[0])
for ticker in tickers:
    print(ticker)
    lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
    rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
              'modules=upgradeDowngradeHistory,recommendationTrend,' \
              'financialData,earningsHistory,earningsTrend,industryTrend&' \
              'corsDomain=finance.yahoo.com'
              
    url =  lhs_url + ticker + rhs_url
    r = requests.get(url)
    if not r.ok:
        recommendation = 6
    try:
        result = r.json()['quoteSummary']['result'][0]
        recommendation =result['financialData']['recommendationMean']['fmt']
    except:
        recommendation = 6
    
    recommendations.append(recommendation)
    
    print("--------------------------------------------")
    print ("{} has an average recommendation of: ".format(ticker), recommendation)
    time.sleep(0.5)
    
dataframe = pd.DataFrame(list(zip(tickers, recommendations)), columns =['Company', 'Recommendations']) 
dataframe = dataframe.set_index('Company')
dataframe.to_csv('recommendations.csv')