#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:21:01 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import cookStock
reload(cookStock)
from cookStock import *

date_from = str(dt.date.today() - dt.timedelta(days=10))
date_to = str(dt.date.today())
x = cookFinancials('GME')

display(x.get_historical_price_data(date_from,date_to, 'daily'))

x.get_ma(str(dt.date.today() - dt.timedelta(days=200)),str(dt.date.today()))
x.get_30day_trend_ma200()

x.get_ma_200(dt.date.today())
x.mv_strategy()
a,b,c,d = x.get_vol(4,50)
x.vol_strategy()
x.price_strategy()
x.combine_strategy()