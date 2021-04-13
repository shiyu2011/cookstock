#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:21:01 2021

@author: sxu
"""
from importlib import reload # python 2.7 does not require this
import sys
sys.path.insert(0, '../src/')
import cookStock
reload(cookStock)
from cookStock import *
import matplotlib.pyplot as plt

generatedDate = '4_9_2021'
generatedInd = 'Service'
name = generatedInd + '_superStocks_' + generatedDate
with open(os.path.join('../result', name+'.json')) as f:
    data = js.load(f)
print(data)
tickers = data['data'][0]


jsfile = os.path.join('../result', name+'_vcp_study.json')
with open(jsfile, "w") as f:
    w = {"data":[]}
    js.dump(w, f, indent = 4)
    
figFolder = os.path.join('../result', 'picture_' + generatedDate, generatedInd)
if not os.path.exists(figFolder):
    os.makedirs(figFolder)
                

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
        
        display(x.get_highest_in5days(date_from))
        
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
            display(footprint)
            print('is a good pivot?')
            isGoodPivot, currentPrice, supportPrice, pressurePrice = x.is_pivot_good()
            display(isGoodPivot)
            print('is a deep correction?')
            isDeepCor = x.is_correction_deep()
            display(isDeepCor)
            print('is demand dried?')
            isDemandDry, startDate, endDate, volume_ls, slope, interY = x.is_demand_dry()
            display(isDemandDry)
            
            s = {ticker:{'current price':str(currentPrice), 'support price':str(supportPrice), 'pressure price':str(pressurePrice), \
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
            
            figName = os.path.join(figFolder, ticker+'.jpg')
            #only save the ones passing all criterion
            if isGoodPivot and not(isDeepCor) and isDemandDry:
                fig.savefig(figName,
                            format='jpeg',
                            dpi=100,
                            bbox_inches='tight')
    except Exception:
        print("error!")
        pass
        #raise
    with open(jsfile, "r") as f:
            data = js.load(f)
            cont = data['data']
            cont.append(s)
    with open(jsfile, "w") as f:
            js.dump(data, f, indent=4) 
            print('=====================================')