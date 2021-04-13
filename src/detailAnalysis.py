#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 22:08:25 2021

@author: sxu
"""
import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd
import os.path
import numpy as np
import json as js
import datetime as dt
import os.path
import re
import time

from importlib import reload # python 2.7 does not require this
import cookStock
reload(cookStock)
from cookStock import *

###load selected stocks

name = 'Heal_superStocks_2_5_2021'
with open(os.path.join('result', name+'.json')) as f:
    data = js.load(f)
print(data)
tickers = data['data'][0]


jsfile = os.path.join('result', name+'_detailed_study.json')
with open(jsfile, "w") as f:
    w = {"data":[]}
    js.dump(w, f, indent = 4)
        


###for each stock
###get the description
###get the foundamental ()
###get the sticker prcie
###get the news
###get the recommendation
s= {}
for ticker in tickers:
    try:
        s["ticker"] = ticker
        display(ticker)
        x = cookFinancials(ticker)
        bv = x.get_BV(20)
        bv.insert(0, x.get_book_value())
        bvgr = x.get_BV_GR_median(bv)
        growth = bvgr[1]
        cEPS = x.get_earnings_per_share()
        years = 3;
        rRate = 0.25;
        safty = 1.0  
        PE = x.get_PE()
        price=x.get_suggest_price(cEPS, growth, years, rRate, PE, safty)
        stickerPrice = x.get_current_price()
        bvq = x.get_BV_quarter()
        qgrowth = x.get_BV_GR_median(bvq)
        roic = x.get_ROIC()
        mcap = x.get_marketCap_B()
        cashflow = (x.get_totalCashFromOperatingActivities())
        priceSales = x.get_pricetoSales()
        
        s = {ticker:{'market cap':mcap, 'value':price[0], 'price':stickerPrice, 'current EPS': cEPS, 'book value anual': bv, 'book value growth': growth,
             'book value quater': bvq, 'book value quater growth': qgrowth[1], 'roic': roic, 'cashflow':cashflow, 'priceSales':priceSales}}    
        
        
        
        
        #https://finance.yahoo.com/quote/DDD/profile?p=DDD
        url = 'https://finance.yahoo.com/quote/'+ticker+'/profile?p='+ticker
        data = urllib2.urlopen(url)      
        soup = BeautifulSoup(data, features = 'lxml')
        summarys = soup.find('p',class_={'Mt(15px) Lh(1.6)'})
        summary = summarys.get_text()
        s[ticker]['business summary']=summary
        
        url = 'https://finance.yahoo.com/quote/'+ticker+'?p='+ticker+'.tsrc=fin-srch'
        data = urllib2.urlopen(url) 
        time.sleep(0.5)
        soup = BeautifulSoup(data, features = 'lxml')
        divs = soup.find('div',attrs={'id':'quoteNewsStream-0-Stream-Proxy'})
        div = divs.find('div',attrs={'id':'quoteNewsStream-0-Stream'})
        ul = div.find('ul')
        lis = ul.findAll('li')
        hls = []
        count = 0
        news = {'news':{}}
        for li in lis:
            # ff = li.find('div', attrs={'class':'C(#959595) Fz(11px) D(ib) Mb(6px)'})
            # dd = ff.findAll('span')
            # tt = ff.find('span')
            title = li.find('a').get_text()
            content = li.find('p').get_text()
            lnk = li.find('a', attrs={'href': re.compile("^https://")})
            news['news'].update({count:{'title':title}})
            news['news'][count].update({'content':content})
            count = count + 1
            
        s[ticker].update(news)
    except Exception:
        print("error!")
        pass
        #raise
    with open(jsfile, "r") as f:
            data = js.load(f)
            cont = data['data']
            cont.append(s)
    with open(jsfile, "w") as f:
            js.dump(data, f, indent=4) 
            print('=====================================')

