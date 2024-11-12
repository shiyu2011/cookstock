#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:21:35 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import os
import sys
#set cookstock path
def find_path():
        home_dir = os.path.expanduser("~")  # Get the home directory
        for root, dirs, files in os.walk(home_dir):  # Walk through the directory structure
            if 'cookstock' in dirs:
                return os.path.join(root, 'cookstock')
        return None  # Return None if the folder was not found

#set cookstock path
basePath = os.path.join(find_path())
#src path
srcPath = os.path.join(basePath, 'src')
print("Adding to sys.path:", srcPath)
sys.path.insert(0, srcPath)

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
#get name of the file from the sector and date automatically
current_date = dt.date.today().strftime("%m_%d_%Y")
file = SectorConstants.TECH + '_superStocks_' + current_date + '.json'

y = batch_process(selected, file)
y.batch_strategy()

###########bio
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.HEALTH_CARE)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.HEALTH_CARE + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()


###########Basics
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.BASICS)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.BASICS + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()

###########services
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.SERVICES)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.SERVICES + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()



###########FINANCE
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.FINANCE)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.FINANCE + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()



###########ENERGY
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.ENERGY)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.ENERGY + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()


###########NON_DURABLE_GOODS
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.NON_DURABLE_GOODS)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.NON_DURABLE_GOODS + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()

###########DURABLE_GOODS
filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.DURABLE_GOODS)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
#filtered_by_sector = ['VNRX', 'INFU']
file = SectorConstants.DURABLE_GOODS + '_superStocks_' + current_date + '.json'
y = batch_process(selected, file)
y.batch_strategy()