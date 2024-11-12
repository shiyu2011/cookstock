#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:20:22 2021

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
import get_tickers
reload(get_tickers)
from get_tickers import *

filtered_by_sector = get_tickers_filtered(sectors=SectorConstants.TECH)

selected = [] 
for i in filtered_by_sector: 
    if i not in selected: 
        selected.append(i) 
        
y = batch_process(selected, 'Tech_basic_11_11_2024.json')
y.batch_financial()
