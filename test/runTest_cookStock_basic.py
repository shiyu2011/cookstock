#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:10:18 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import sys
sys.path.insert(0, '../src/')
import cookStock
reload(cookStock)
from cookStock import *
import pandas as pd

x = cookFinancials('GME')

display(x.get_balanceSheetHistory_quarter())

display(x.get_incomeStatementHistory_quarter())

display(x.get_cashflowStatementHistory_quarter())

display(x.get_BV_quarter())

display(x.get_summary_data())

bv = x.get_BV_quarter()
display(x.get_GR_median(bv))
display(x.get_earningsperShare())

bv = x.get_BV()
display(x.get_GR_median(bv))

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