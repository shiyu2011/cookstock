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
import matplotlib
matplotlib.use('Agg')


date_from = (dt.date.today() - dt.timedelta(days=100))
date_to = (dt.date.today())
x = cookFinancials('TSLA')

print(x.get_ma(date_from, date_to))
print(x.get_ma_ref(date_from, date_to))
print(x.get_ma_50(date_to))
s = x.get_price(date_from, 100)
tmpLen = len(s)
date = []
price = []
volume = []
for i in range(tmpLen):
    date.append(s[i]['formatted_date'])
    price.append(s[i]['close'])
    volume.append(s[i]['volume'])
%matplotlib qt



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
    
    ax[0].set_xticks(np.arange(0, len(date)+1, 10))
    ax[1].set_xticks(np.arange(0, len(date)+1, 10))
    
    
    # save the plot as a file
    # fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
    #             format='jpeg',
    #             dpi=100,
    #             bbox_inches='tight')
    print('footprint:')
    display(x.get_footPrint())
    print('is a good pivot?')
    display(x.is_pivot_good())
    print('is a deep correction?')
    display(x.is_correction_deep())
    print('is demand dried?')
    flag, startDate, endDate, volume_ls, slope, interY = x.is_demand_dry()
    display(flag)
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
    #fig.show()

    


# ##find 1
# flag, hD, hP, lD, lP = x.find_one_contraction(date_from)
# flag = x.find_one_contraction(date_from)

# plt.plot([hD, lD], [hP, lP], 'r')

# ##find 2
# lD_tmp = dt.datetime.strptime(lD, "%Y-%m-%d")
# lD_dt = lD_tmp.date()
# hD1, hP1, lD1, lP1 = x.find_one_contraction(lD_dt)
# plt.plot([hD1, lD1], [hP1, lP1], 'r')

# ##find 3
# lD1_tmp = dt.datetime.strptime(lD1, "%Y-%m-%d")
# lD1_dt = lD1_tmp.date()
# hD2, hP2, lD2, lP2 = x.find_one_contraction(lD1_dt)
# plt.plot([hD2, lD2], [hP2, lP2], 'r')
# plt.show()

# display(x.get_historical_price_data(date_from,date_to, 'daily'))

# x.get_ma(str(dt.date.today() - dt.timedelta(days=200)),str(dt.date.today()))
# x.get_30day_trend_ma200()

# x.get_ma_200(dt.date.today())
# x.mv_strategy()
# a,b,c,d = x.get_vol(4,50)
# x.vol_strategy()
# x.price_strategy()
# x.combine_strategy()