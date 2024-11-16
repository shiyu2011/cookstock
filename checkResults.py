import json
import sys
import os
#load specified json
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

import cookStock
from cookStock import *

folder = os.path.join(basePath, 'results', '2024-11-14')
file = os.path.join(folder, 'Technology_HealthCare_BasicIndustries_ConsumerServices_Finance_Energy_ConsumerNon-Durables_ConsumerDurables.json')
with open(file, 'r') as f:
    data = json.load(f)

for entry in data["data"]:
    for ticker, details in entry.items():
        #get current price of the stock
        print(ticker)
        x = cookFinancials(ticker)
        s = x.get_current_price()
        # Convert details['current price'] to float
        current_price_in_data = float(details['current price'])
        print(current_price_in_data)
        print(s)
        current_price_at_check = s
        details['current price'] = current_price_at_check
        change = (current_price_at_check - current_price_in_data) / current_price_in_data
        details['change'] = change
        print("-----")

#order based on change
data["data"].sort(key=lambda x: list(x.values())[0]['change'], reverse=True)

#save the json file
file = os.path.join(basePath, 'tmp.json')
with open(file, 'w') as f:
    json.dump(data, f, indent=4)