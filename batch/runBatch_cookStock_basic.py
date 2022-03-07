#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:20:22 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import sys
sys.path.insert(0, '/Users/sxu/deeppath/stock/cookstock/src/')
import cookStock
reload(cookStock)
from cookStock import *
import get_tickers
reload(get_tickers)
from get_tickers import *

filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.TECH)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
y = batch_process(selected, 'Tech_basic_3_6_2022.json')
y.batch_financial()
