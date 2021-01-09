#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:57:10 2021

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

#ready json file to get ticker
with open(os.path.join('result', 'Health_superStocks_1_7_2021.json')) as f:
  data = js.load(f)
print(data)

tickers = data['data'][0]
news = []

for ticker in tickers:
    try:
        print(ticker)
        url = 'https://finance.yahoo.com/quote/'+ticker+'?p='+ticker+'.tsrc=fin-srch'
        data = urllib2.urlopen(url)
        soup = BeautifulSoup(data)
        divs = soup.find('div',attrs={'id':'quoteNewsStream-0-Stream-Proxy'})
        div = divs.find('div',attrs={'id':'quoteNewsStream-0-Stream'})
        ul = div.find('ul')
        lis = ul.findAll('li')
        hls = []
        count = 0
        s = {ticker:[]}
        for li in lis:
            headlines = li.find('a').contents
            s[ticker].append(headlines)
        news.append(s)
    except Exception:
        print("error!")
        pass

display(news)
# df = pd.DataFrame(news)
# with pd.option_context('display.max_colwidth', 10):
#     display(df)

import tempfile
import webbrowser

html = '<html>'+str(news)+'</html>'

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    url = 'file://' + f.name
    f.write(html)
webbrowser.open(url)