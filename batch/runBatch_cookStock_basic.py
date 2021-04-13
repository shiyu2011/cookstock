#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:20:22 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import sys
sys.path.insert(0, '../src/')
import cookStock
reload(cookStock)
from cookStock import *
from get_all_tickers import get_tickers as gt
from get_all_tickers.get_tickers import Region

tickers = gt.get_tickers()

filtered_by_sector = gt.get_tickers_filtered(sectors=gt.SectorConstants.TECH)
filtered_by_sector
y = batch_process(filtered_by_sector, 'Tech_basic_1_12_2021.json')
y.batch_financial()
