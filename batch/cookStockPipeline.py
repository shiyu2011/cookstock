###a high level script to run the whole pipeline
# runBatch_cookStock_stage2template.py
# get super stocks
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday 11/12/2024

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

import matplotlib.pyplot as plt
import cookStock
reload(cookStock)
from cookStock import *


from importlib import reload # python 2.7 does not require this
import get_tickers
reload(get_tickers)
from get_tickers import *

        
#filtered_by_sector = ['VNRX', 'INFU']
#get name of the file from the sector and date automatically
current_date = dt.date.today().strftime("%m_%d_%Y")

#set sector names to be run
# sectorCollection = [SectorConstants.TECH, SectorConstants.HEALTH_CARE, SectorConstants.BASICS, SectorConstants.SERVICES, SectorConstants.FINANCE, SectorConstants.ENERGY, SectorConstants.NON_DURABLE_GOODS, SectorConstants.DURABLE_GOODS]

sectorCollection = [SectorConstants.TECH, SectorConstants.HEALTH_CARE,SectorConstants.FINANCE, SectorConstants.ENERGY]

# sectorCollection = [SectorConstants.TECH]

sectorName = []
selected = [] 
for sector in sectorCollection:
    filtered_by_sector = get_tickers_filtered(sectors=sector)
    #remove underscore in sector name
    sector = sector.replace(" ", "")
    sectorName.append(sector)
    for i in filtered_by_sector: 
        if i not in selected: 
            selected.append(i) 

#convert sectorCollection to a file name
sectorNameStr = '_'.join(sectorName)

# selected = ['VNRX', 'INFU']

y = batch_process(selected, sectorNameStr)
y.batch_pipeline_full()


def load_json(filepath):
    with open(filepath, "r") as f:
        return js.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        js.dump(data, f, indent=4)

def append_to_json(filepath, ticker_data):
    data = load_json(filepath)
    data['data'].append(ticker_data)
    save_json(filepath, data)

def setup_result_file(basePath, file_prefix, current_date):
    filepath = os.path.join(basePath, 'results', f"{file_prefix}_vcp_study_{current_date}.json")
    save_json(filepath, {"data": []})
    return filepath