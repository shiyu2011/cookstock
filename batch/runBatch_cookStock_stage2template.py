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

#set sector names to be run
sectorCollection = [SectorConstants.TECH, SectorConstants.HEALTH_CARE, SectorConstants.BASICS, SectorConstants.SERVICES, SectorConstants.FINANCE, SectorConstants.ENERGY, SectorConstants.NON_DURABLE_GOODS, SectorConstants.DURABLE_GOODS]

for sector in sectorCollection:
    filtered_by_sector = get_tickers_filtered(sectors=sector)
    selected = [] 
    for i in filtered_by_sector: 
        if i not in selected: 
            selected.append(i) 
    file = sector + '_superStocks_' + current_date + '.json'
    print('start processing ' + sector)
    y = batch_process(selected, file)
    y.batch_strategy()
    print('end processing ' + sector)
    print('----------------------------------')