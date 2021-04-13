#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:21:35 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import sys
sys.path.insert(0, '../src/')
import cookStock
reload(cookStock)
from cookStock import *


from importlib import reload # python 2.7 does not require this
import get_tickers
reload(get_tickers)
from get_tickers import *

tmp = get_tickers(NYSE=True, NASDAQ=True, AMEX=True)

tickers = [] 
for i in tmp: 
    if i not in tickers: 
        tickers.append(i) 
        
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.TECH)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
y = batch_process(selected, 'Tech_superStocks_4_12_2021.json')
y.batch_strategy()

###########bio
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.HEALTH_CARE)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
y = batch_process(selected, 'Heal_superStocks_4_12_2021.json')
y.batch_strategy()


###########Basics
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.BASICS)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
y = batch_process(selected, 'Basic_superStocks_4_12_2021.json')
y.batch_strategy()

###########Basics
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.SERVICES)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
y = batch_process(selected, 'Service_superStocks_4_12_2021.json')
y.batch_strategy()