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

x = cookFinancials('RIOT')
x.get_ma(str(dt.date.today() - dt.timedelta(days=200)),str(dt.date.today()))
x.get_30day_trend_ma200()

x.get_ma_200(dt.date.today())
x.mv_strategy()
a,b,c,d = x.get_vol(4,50)
x.vol_strategy()
x.price_strategy()
x.combine_strategy()