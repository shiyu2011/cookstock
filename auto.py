import json
import os
import datetime as dt
import sys


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
from cookStock import *

# get all folders under results, access order from latest to oldest, in each folder read the json file and get the data
folderList = []  # Initialize an empty list to store folder names and dates
for root, dirs, files in os.walk('results'):
    for folder in dirs:
        print(folder)
        
        try:
            # Attempt to parse the folder name as a date
            date = dt.datetime.strptime(folder, '%Y-%m-%d')
            print(date)
            folderList.append((folder, date))  # Append folder name and date as a tuple
        except ValueError:
            # If the folder name is not a date, skip it
            print(f"Skipping folder '{folder}' - not in 'YYYY-MM-DD' format.")
            continue


# sort the folderList by date
folderList.sort(key=lambda x: x[1], reverse=True)

# loop through each folder and read the json file
# define a list to store the combined data
combinedData = {"data": []}
for folder, date in folderList:
    jsonFile = os.path.join('results', folder, 'Technology_HealthCare_BasicIndustries_ConsumerServices_Finance_Energy_ConsumerNon-Durables_ConsumerDurables.json')
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    for entry in data["data"]:
        for ticker, details in entry.items():
            #get current price of the stock
            print(ticker)
            x = cookFinancials(ticker)
            s = x.get_current_price()
            # Convert details['current price'] to float
            current_price_in_data = float(details['current price'])
            #add/udpate the current price to the details
            details['current price at Check'] = s
            #calculate the percentage of change
            price_change = (s - current_price_in_data) / current_price_in_data    
            #add/update the price change to the details
            details['price_change'] = price_change
            #add/update the date to the details
            details['date of the selection'] = date.strftime('%m/%d/%Y')
            #add current time to the details
            details['time at Check'] = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            #append the entry to the combinedData
            combinedData['data'].append({ticker: details})

#sort the combinedData based on price change
combinedData['data'] = sorted(combinedData['data'], key=lambda x: x[list(x.keys())[0]]['price_change'], reverse=True)
#write the sorted data to a file
with open('results/combinedData.json', 'w') as f:
    json.dump(combinedData, f, indent=4)
    print(f"Combined data written to 'results/combinedData.json'")
        
# loop each folder and read the json file
readme_content = "# Daily Stock Analysis\n\n"
readme_content += "This report provides an overview of selected stocks with volatility contraction patterns and analysis details.\n\n"
readme_content += "## Stocks Overview\n\n"

#load the cobminedData to generate the readme file
with open('results/combinedData.json', 'r') as f:
    combinedData = json.load(f)
for entry in combinedData["data"]:
    for ticker, details in entry.items():
        readme_content += "### " + ticker + "\n"
        readme_content += f"- **Current Price during run time**: {details['current price']}\n"
        readme_content += f"- **Support Price**: {details['support price']}\n"
        readme_content += f"- **Pressure Price**: {details['pressure price']}\n"
        readme_content += f"- **Good Pivot**: {details['is_good_pivot']}\n"
        readme_content += f"- **Deep Correction**: {details['is_deep_correction']}\n"
        readme_content += f"- **Demand Dry**: {details['is_demand_dry']}\n"
        readme_content += f"- **Current Price at Check**: {details['current price at Check']}\n"
        readme_content += f"- **Price Change**: {details['price_change']:.4%}\n"
        readme_content += f"- **Date of the Selection**: {details['date of the selection']}\n"
        readme_content += f"- **Time at Check**: {details['time at Check']}\n\n"
        # Add image if it exists
        if 'fig' in details:
            # Extract the path starting from 'results'
            fig_path = details['fig']
            img_path = os.path.relpath(fig_path, start='/home/rxm/cookstock/results')
            readme_content += f"![{ticker} Chart](./{img_path})\n"
        readme_content += "\n"  


# write the readme file
readme_file = os.path.join('results', 'README.md')

with open(readme_file, 'w') as f:
    f.write(readme_content)
    print(f"README file written to '{readme_file}'")
    
    
