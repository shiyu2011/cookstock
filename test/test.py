#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:23:57 2021

@author: sxu
"""
from get_all_tickers import get_tickers as gt
from get_all_tickers.get_tickers import Region

from importlib import reload # python 2.7 does not require this
import get_tickers
reload(get_tickers)
from get_tickers import *

tickers = get_tickers()