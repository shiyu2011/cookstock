import json
import os
import datetime as dt

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
 

# loop each folder and read the json file
readme_content = "# Daily Stock Analysis\n\n"
readme_content += "This report provides an overview of selected stocks with volatility contraction patterns and analysis details.\n\n"
readme_content += "## Stocks Overview\n\n"

for folder, date in folderList:
    print(folder)
    # get the json file
    jsonFile = os.path.join('results', folder, 'Technology_HealthCare_BasicIndustries_ConsumerServices_Finance_Energy_ConsumerNon-Durables_ConsumerDurables.json')
    print(jsonFile)
    # add date in the readme
    readme_content += "### " + date.strftime('%m/%d/%Y') + "\n\n"
    with open(jsonFile, 'r') as f:
        data = json.load(f)
        print(data)
        
    for entry in data["data"]:
        for ticker, details in entry.items():
            readme_content += "#### " + ticker + "\n"
            readme_content += f"- **Current Price**: {details['current price']}\n"
            readme_content += f"- **Support Price**: {details['support price']}\n"
            readme_content += f"- **Pressure Price**: {details['pressure price']}\n"
            readme_content += f"- **Good Pivot**: {details['is_good_pivot']}\n"
            readme_content += f"- **Deep Correction**: {details['is_deep_correction']}\n"
            readme_content += f"- **Demand Dry**: {details['is_demand_dry']}\n"
            
            # Add image if it exists
            if 'fig' in details:
                img_path = os.path.join(folder, os.path.basename(details['fig']))
                readme_content += f"![{ticker} Chart](./{img_path})\n"
            
            readme_content += "\n"

# write the readme file
readme_file = os.path.join('results', 'README.md')

with open(readme_file, 'w') as f:
    f.write(readme_content)
    print(f"README file written to '{readme_file}'")
    
    
