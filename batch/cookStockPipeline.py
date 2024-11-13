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

# sectorCollection = [SectorConstants.TECH]


for sector in sectorCollection:
    filtered_by_sector = get_tickers_filtered(sectors=sector)
    selected = [] 
    for i in filtered_by_sector: 
        if i not in selected: 
            selected.append(i) 
    #replace space in sector name with underscore
    sector = sector.replace(" ", "")
    file = sector + '_superStocks_' + current_date + '.json'
    print('start processing ' + sector)
    y = batch_process(selected, file)
    y.batch_strategy()
    print('end processing ' + sector)
    print('----------------------------------')

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

# runBatch_volatility_contraction_pattern.py
# get the stocks that have volatility contraction pattern and save the figure
#load all the super stock files
# get fiies with pattern *superStocks*current_date*.json
files = [f for f in os.listdir(os.path.join(basePath, 'results')) if 'superStocks' in f and current_date in f]
#loop through each file and get the tickers
for file in files:
    data = load_json(os.path.join(basePath, 'results', file))
    tickers = data['data'][0]
        
    result_file = setup_result_file(basePath, file.split('_')[0], current_date)
    fig_folder = os.path.join(basePath, 'results', f"picture_{current_date}", file.split('_')[0])
    os.makedirs(fig_folder, exist_ok=True)
    
        
    date_from = (dt.date.today() - dt.timedelta(days=100))
    date_to = (dt.date.today())
    s= {}
    #%matplotlib inline
    for ticker in tickers:
        try:
            x = cookFinancials(ticker)   
            sp = x.get_price(date_from, 100)
            tmpLen = len(sp)
            date = []
            price = []
            volume = []
            for i in range(tmpLen):
                date.append(sp[i]['formatted_date'])
                price.append(sp[i]['close'])
                volume.append(sp[i]['volume'])
                

            
            # create figure and axis objects with subplots()
            fig,ax = plt.subplots(2)
            fig.suptitle(x.ticker)
            # make a plot
            ax[0].plot(date, price, color="blue", marker="o")
            # set x-axis label
            ax[0].set_xlabel("date",fontsize=14)
            # set y-axis label
            ax[0].set_ylabel("stock price",color="blue",fontsize=14)
            
            # twin object for two different y-axis on the sample plot
            # make a plot with different y-axis using second axis object
            ax[1].bar(date, np.asarray(volume)/10**6 ,color="green")
            ax[1].set_ylabel("volume (m)",color="green",fontsize=14)
            #ax[1].set_ylim([0, 100])
            
            print(x.get_highest_in5days(date_from))
            
            counter, record = x.find_volatility_contraction_pattern(date_from)
            
            if counter > 0:
                for i in range(counter):
                    ax[0].plot([record[i][0], record[i][2]], [record[i][1], record[i][3]], 'r')
                
                ax[0].set_xticks(np.arange(0, len(date)+1, 12))
                ax[1].set_xticks(np.arange(0, len(date)+1, 12))
                
                
                # save the plot as a file
                # fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
                #             format='jpeg',
                #             dpi=100,
                #             bbox_inches='tight')
                print('footprint:')
                footprint = x.get_footPrint()
                print(footprint)
                print('is a good pivot?')
                isGoodPivot, currentPrice, supportPrice, pressurePrice = x.is_pivot_good()
                print(isGoodPivot)
                print('is a deep correction?')
                isDeepCor = x.is_correction_deep()
                print(isDeepCor)
                print('is demand dried?')
                isDemandDry, startDate, endDate, volume_ls, slope, interY = x.is_demand_dry()
                print(isDemandDry)
                
                ticker_data = {ticker:{'current price':str(currentPrice), 'support price':str(supportPrice), 'pressure price':str(pressurePrice), \
                            'is_good_pivot':str(isGoodPivot), 'is_deep_correction':str(isDeepCor), 'is_demand_dry': str(isDemandDry)}}    

                for ind, item in enumerate(date):
                    if item == startDate:
                        print(ind)
                        break
                #ax[1].plot()
                x_axis = []
                for i in range(len(volume_ls)):
                    x_axis.append(ind+i)
                x_axis = np.array(x_axis)
                y = slope*x_axis-slope*ind + volume_ls[0]
                ax[1].plot(np.asarray(date)[x_axis], y/10**6, color="red",linewidth=4)
                fig.show()
                
                figName = os.path.join(fig_folder, ticker+'.jpg')
                #only save the ones passing all criterion
                if isGoodPivot and not(isDeepCor) and isDemandDry:
                    fig.savefig(figName,
                                format='jpeg',
                                dpi=100,
                                bbox_inches='tight')
                    #add link to the json file
                    ticker_data[ticker]['fig'] = figName
                    #add set a flag to indicate the stock has potential to boom
                    ticker_data[ticker]['boomFlag'] = True
                    
                append_to_json(result_file, ticker_data)
        except Exception:
            print("error!")
            pass

# for each file



# get details analysis using detailAnalysis.py


# get recommendation using recommendationExtract.py for the stocks that have volatility contraction pattern