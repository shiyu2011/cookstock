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
import re

#ready json file to get ticker
with open(os.path.join('result', 'Tech_superStocks_1_12_2021.json')) as f:
  data = js.load(f)
print(data)

tickers = data['data'][0]
news = []

for ticker in tickers:
    try:
        display(ticker)
        url = 'https://finance.yahoo.com/quote/'+ticker+'?p='+ticker+'.tsrc=fin-srch'
        data = urllib2.urlopen(url)
        soup = BeautifulSoup(data, features = 'html.parser')
        divs = soup.find('div',attrs={'id':'quoteNewsStream-0-Stream-Proxy'})
        div = divs.find('div',attrs={'id':'quoteNewsStream-0-Stream'})
        ul = div.find('ul')
        lis = ul.findAll('li')
        hls = []
        count = 0
        s = {ticker:[]}
        for li in lis:
            ff = li.find('div', attrs={'class':'C(#959595) Fz(11px) D(ib) Mb(6px)'})
            dd = ff.findAll('span')
            #tt = ff.find('span')
            title = li.find('a')
            content = li.find('p')
            lnk = li.find('a', attrs={'href': re.compile("^https://")})
            
            #display(tt.get_text())
            display('***********************************************')
            display(dd)
            display('*title*')
            display(title.get_text())
            display(lnk)
            display('*content*')
            display(content.get_text())
            #display(title.get_text())
            #display(lnk)
            #s[ticker].append(headlines)
        #news.append(s)
    except Exception:
        print("error!")
        pass
    display('***********************************************')
    display('///////////////////////////////////////////////')

display(news)
# df = pd.DataFrame(news)
# with pd.option_context('display.max_colwidth', 10):
#     display(df)

# import tempfile
# import webbrowser

# html = '<html>'+str(news)+'</html>'

# with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
#     url = 'file://' + f.name
#     f.write(html)
# webbrowser.open(url)