#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:10:18 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import sys
import os

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

#how to get the path right
#where I am running the code from
print("Adding to sys.path:", srcPath)
sys.path.insert(0, srcPath)


import cookStock
reload(cookStock)
from cookStock import *
import pandas as pd

x = cookFinancials('AAPL')

print(x.get_balanceSheetHistory_quarter())

print(x.get_incomeStatementHistory_quarter())

print(x.get_cashflowStatementHistory_quarter())

print(x.get_BV_quarter())

print(x.get_summary_data())

bv = x.get_BV_quarter()
print(x.get_GR_median(bv))
print(x.get_earningsperShare())

bv = x.get_BV()
print(x.get_GR_median(bv))

bv = x.get_BV(20)
bv.insert(0, x.get_book_value())
print(x.ticker,'book value',bv)
bvgr = x.get_BV_GR_median(bv)
print(bvgr)
growth = bvgr[1]
cEPS = x.get_earnings_per_share()
years = 3;
rRate = 0.25;
safty = 0.5
PE = x.get_PE()
price=x.get_suggest_price(cEPS, growth, years, rRate, PE, safty)                
print(price)
stickerPrice = x.get_current_price()
decision = x.get_decision(price[1],stickerPrice)
print(decision)