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
#load combinedData.json and remove duplicates stickers with the same date of the selection
file = os.path.join(basePath, 'results', 'combinedData.json')
with open(file, 'r') as f:
    data = json.load(f)
    
#loop all entries and remove duplicates
uniqueData = {"data": []}
uniqueTickers = []
for entry in data["data"]:
    for ticker, details in entry.items():
        if ticker not in uniqueTickers:
            uniqueTickers.append(ticker)
            uniqueData["data"].append({ticker: details})
        else:
            #check if the date is the same
            for uniqueEntry in uniqueData["data"]:
                for uniqueTicker, uniqueDetails in uniqueEntry.items():
                    if uniqueTicker == ticker:
                        if uniqueDetails['date of the selection'] == details['date of the selection']:
                            print(f"Duplicate sticker {ticker} with the same date of the selection {details['date of the selection']} removed.")
                        else:
                            uniqueData["data"].append({ticker: details})
                            uniqueTickers.append(ticker)
                            
#save the uniqueData to a file
file = os.path.join(basePath, 'results', 'combinedData.json')
with open(file, 'w') as f:
    json.dump(uniqueData, f, indent=4)
    
# loop each folder and read the json file
readme_content = "# Daily Stock Analysis\n\n"
readme_content += "This report provides an overview of selected stocks with volatility contraction patterns and analysis details.\n\n"
readme_content += "## Stocks Overview\n\n"

#load the cobminedData to generate the readme file
with open(file, 'r') as f:
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
readme_file = os.path.join(basePath, 'results', 'README.md')

with open(readme_file, 'w') as f:
    f.write(readme_content)
    print(f"README file written to '{readme_file}'")