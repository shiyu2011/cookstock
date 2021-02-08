#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:21:35 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import cookStock
reload(cookStock)
from cookStock import *


from importlib import reload # python 2.7 does not require this
import get_tickers
reload(get_tickers)
from get_tickers import *

tmp = get_tickers(NYSE=False, NASDAQ=True, AMEX=False)

tickers = [] 
for i in tmp: 
    if i not in tickers: 
        tickers.append(i) 

filtered_by_sector = get_tickers_filtered(sectors=gt.SectorConstants.TECH)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
y = batch_process(selected, 'Tech_superStocks_2_5_2021.json')
y.batch_strategy()