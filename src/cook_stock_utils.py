import json
import os
import datetime as dt
import sys
import glob

def find_path():
    """Find the base path of the 'cookstock' directory."""
    home_dir = os.path.expanduser("~")
    for root, dirs, files in os.walk(home_dir):
        if 'cookstock' in dirs:
            return os.path.join(root, 'cookstock')
    return None

#set cookstock path
basePath = os.path.join(find_path())
#src path
srcPath = os.path.join(basePath, 'src')
print("Adding to sys.path:", srcPath)
sys.path.insert(0, srcPath)
import cookStock
from cookStock import *


def read_json(file_path):
    """Read a JSON file and return its content."""
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"JSON saved to '{file_path}'")
    
def append_to_json(filepath, ticker_data):
    data = read_json(filepath)
    ticker = list(ticker_data.keys())[0]  # Get the ticker name
    updated = False

    # Check if the ticker already exists in the data
    for entry in data['data']:
        if ticker in entry:  # If ticker exists, update it
            entry[ticker] = ticker_data[ticker]
            updated = True
            break

    if not updated:  # If ticker does not exist, append it
        data['data'].append(ticker_data)

    save_json(filepath, data)

def search_use_key(data, ticker):
    for entry in data['data']:
        if ticker in entry:
            return entry[ticker]
    return None 

def get_selected_tickers_details(data, tickers):
    selectedTickers = []
    for ticker in tickers:
        details = search_use_key(data, ticker)
        if details:
            selectedTickers.append({ticker: details})
    return selectedTickers


def merge_data(combinedData, filteredData):
    for entry in filteredData['data']:
        for ticker, details in entry.items():
            # Use ticker as the key to check if the ticker already exists in the combinedData
            existingData = search_use_key(combinedData, ticker)
            if existingData:
                # Ensure 'news' key exists in existingData
                if 'news' not in existingData:
                    existingData['news'] = []  # Initialize as an empty list
                
                # Get news from entry
                news = details.get('news', [])  # Get news from the details, default to empty list
                
                # Loop through the news and append the title, review, and date
                for news_item in news:
                    title = news_item.get('title', 'No Title')
                    review = news_item.get('review', 'No Review')
                    date = news_item.get('date', 'No Date')
                    
                    # Append the news to the existingData
                    existingData['news'].append({'title': title, 'review': review, 'date': date})
                
                # Update combinedData with the modified existingData
                for combined_entry in combinedData['data']:
                    if ticker in combined_entry:
                        combined_entry[ticker] = existingData
                        break
            else:
                # If ticker doesn't exist in combinedData, append it
                combinedData['data'].append({ticker: details})
    
    return combinedData

from html import escape

def write_html(basePath, newCombinedData):
    data = newCombinedData['data']
    current_date = dt.date.today().strftime("%m_%d_%Y")
    
    # HTML header
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily Stock Analysis: {current_date}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                font-size: 24px;
                margin-bottom: 10px;
            }}
            h2 {{
                font-size: 20px;
                margin-bottom: 10px;
            }}
            h3 {{
                font-size: 16px;
                margin-bottom: 10px;
            }}
            p {{
                margin-bottom: 10px;
            }}
            .stock {{
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ccc;
            }}
            .news {{
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid #ccc;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Daily Stock Analysis: {current_date}</h1>
            <p>This report provides an overview of selected stocks with volatility contraction patterns and analysis details.</p>
            <h2>Stocks Overview</h2>
    """

    # Generate content for each stock
    for entry in data:
        for ticker, details in entry.items():
            html_content += f"""
            <div class="stock">
                <h3>{escape(ticker)}</h3>
                <p><strong>Current Price during run time:</strong> {escape(details.get('current price', 'N/A'))}</p>
                <p><strong>Support Price:</strong> {escape(details.get('support price', 'N/A'))}</p>
                <p><strong>Pressure Price:</strong> {escape(details.get('pressure price', 'N/A'))}</p>
                <p><strong>Good Pivot:</strong> {escape(details.get('is_good_pivot', 'N/A'))}</p>
                <p><strong>Deep Correction:</strong> {escape(details.get('is_deep_correction', 'N/A'))}</p>
                <p><strong>Demand Dry:</strong> {escape(details.get('is_demand_dry', 'N/A'))}</p>
                <p><strong>Current Price at Check:</strong> {escape(str(details.get('current price at Check', 'N/A')))}</p>                <p><strong>Price Change:</strong> {details.get('price_change', 0):.4%}</p>
                <p><strong>Date of the Selection:</strong> {escape(details.get('date of the selection', 'N/A'))}</p>
                <p><strong>Time at Check:</strong> {escape(details.get('time at Check', 'N/A'))}</p>
            """
            # Add news section
            news = details.get('news', [])
            if news:
                html_content += """<div class="news"><h4>News</h4>"""
                for article in news:
                    html_content += f"""
                    <p><strong>{escape(article.get('title', 'No Title'))}</strong><br>
                    {escape(article.get('summary', 'No Summary'))}<br>
                    <a href="{escape(article.get('url', '#'))}">Read more</a></p>
                    """
                html_content += "</div>"
            else:
                html_content += "<p>No news available</p>"

            # Add image if available
            fig_path = details.get('fig')
            if fig_path:
                prefix_to_remove = os.path.join(basePath, 'results')
                img_path = fig_path.replace(prefix_to_remove, '').lstrip(os.sep)
                html_content += f"""
                <img src="./{escape(img_path)}" alt="{escape(ticker)} Chart">
                """

            html_content += "</div>"

    # Close the container div and HTML
    html_content += """
        </div>
    </body>
    </html>
    """

    # Save the HTML content to a file
    output_path = os.path.join(basePath, 'results', 'report.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
   
                    

def write_readme(basePath, newCombinedData):
    data = newCombinedData['data']
    current_date = dt.date.today().strftime("%m_%d_%Y")
    # loop each folder and read the json file
    readme_content = f"# Daily Stock Analysis: {current_date}\n\n"

    readme_content += f"This report provides an overview of selected stocks with volatility contraction patterns and analysis details.\n\n"
    readme_content += f"## Stocks Overview\n\n"

    for entry in data:
        for ticker, details in entry.items():
            readme_content += "### " + ticker + "\n"
            readme_content += f"- **Current Price during run time**: {details['current price']}\n"
            readme_content += f"- **Support Price**: {details['support price']}\n"
            readme_content += f"- **Pressure Price**: {details['pressure price']}\n"
            readme_content += f"- **Good Pivot**: {details['is_good_pivot']}\n"
            readme_content += f"- **Deep Correction**: {details['is_deep_correction']}\n"
            readme_content += f"- **Demand Dry**: {details['is_demand_dry']}\n"
            #check if the current price at check exists
            if 'current price at Check' in details:
                readme_content += f"- **Current Price at Check**: {details['current price at Check']}\n"
                readme_content += f"- **Price Change**: {details['price_change']:.4%}\n"
                if 'date of the selection' in details:
                    readme_content += f"- **Date of the Selection**: {details['date of the selection']}\n"
                readme_content += f"- **Time at Check**: {details['time at Check']}\n"

            readme_content += "#### News\n"
            if 'news' in details:
                for news_item in details['news']:
                    readme_content += f"##### {news_item['title']} ({news_item['date']})\n"
                    readme_content += f"{news_item['review']}\n\n"
            else:
                readme_content += "No news available\n\n"
            # Add image if it exists
            if 'fig' in details:
                # Extract the path starting from 'results'
                fig_path = details['fig']  # Example full path
                prefix_to_remove = os.path.join(basePath, 'results')  # Prefix to remove
                # Remove the prefix
                img_path = fig_path.replace(prefix_to_remove, '', 1) 
                readme_content += f"![{ticker} Chart](./{img_path})\n"
            readme_content += "\n"  

    with open(os.path.join(basePath, 'results', 'README_full.md'), 'w') as f:
        f.write(readme_content)

def check_current_price_from_raw_selections(base_path, folder_name, json_file_name, output_file_name):
    """Prepare JSON data by updating the current price and change percentage."""
    folder = os.path.join(base_path, 'results', folder_name)
    file_path = os.path.join(folder, json_file_name)
    data = read_json(file_path)

    for entry in data["data"]:
        for ticker, details in entry.items():
            print(f"Processing ticker: {ticker}")
            x = cookFinancials(ticker)
            s = x.get_current_price()
            current_price_in_data = float(details['current price'])
            details['current price at check'] = s
            details['change'] = (s - current_price_in_data) / current_price_in_data
            details['time at Check'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Updated {ticker}: Current Price: {s}, Change: {details['change']:.4%}")

    # Sort data based on change percentage
    data["data"].sort(key=lambda x: list(x.values())[0]['change'], reverse=True)

    # Save the updated JSON
    output_file = os.path.join(base_path, 'tmp', output_file_name)
    save_json(data, output_file)

def check_if_duplicates(json_file):
    """Check if there are any duplicate entries in a JSON file."""
    data = read_json(json_file)
    tickers = [list(entry.keys())[0] for entry in data["data"]]
    return len(tickers) != len(set(tickers))


def check_and_remove_duplicates(json_file):
    """Remove duplicate tickers from a JSON file."""
    print(f"Checking for duplicates in {json_file}...")
    data = read_json(json_file)
    unique_data = {"data": []}
    seen_tickers = set()

    for entry in data["data"]:
        for ticker, _ in entry.items():
            if ticker not in seen_tickers:
                unique_data["data"].append(entry)
                seen_tickers.add(ticker)

    save_json(unique_data, json_file)
    print(f"Duplicates removed from {json_file}")


def count_tickers(json_file):
    """Count the total number of entries in a JSON file."""
    data = read_json(json_file)
    tickers = [list(entry.keys())[0] for entry in data["data"]]
    print(f"Total tickers: {len(tickers)}")
    print(f"Unique tickers: {len(set(tickers))}")
    return len(tickers)

def create_combinedJson_addCurrentPrice_fromAllFolders():
    # get all folders under results, access order from latest to oldest, in each folder read the json file and get the data
    folderList = []  # Initialize an empty list to store folder names and dates
    resultsPath = os.path.join(basePath, 'results')
    for _, dirs, _ in os.walk(resultsPath):
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
        jsonFile = glob.glob(os.path.join(basePath, 'results', folder, 'Technology*.json'))
        with open(jsonFile[0], 'r') as f:
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
                #add/update the price change to the sdetails
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
    file = os.path.join(basePath, 'results', 'combinedData.json')
    #want to overwrite the file, delete it first
    save_json(combinedData, file)
    
def add_current_price(file):
    """Add the current price of the stocks to the combinedData_gpt.json file."""
    data = read_json(file)
    for entry in data['data']:
        for ticker, details in entry.items():
            print(f"Processing ticker: {ticker}")
            x = cookFinancials(ticker)
            current_price = x.get_current_price()
            details['current price at Check'] = current_price
            price_change = (current_price - float(details['current price'])) / float(details['current price'])
            details['price_change'] = price_change
            details['time at Check'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Sort data based on price change
    data['data'].sort(key=lambda x: list(x.values())[0]['price_change'], reverse=True)
    save_json(data, file)
    return data

# Example usage
if __name__ == "__main__":
    basePath = find_path()

    # # 2:00 am run
    combinedData = os.path.join(basePath, 'results', '2024-12-03/Technology_HealthCare_Finance_Energy.json')
    filteredData = os.path.join(basePath, 'results', 'filteredData_gpt.json')
    newCombinedData = merge_data(load_json(combinedData), load_json(filteredData))
    write_readme(basePath, newCombinedData)
    
    ## moring before 6:30 am run to generate the report into readme markdown file
    
    
    
    # 1:00 pm run
    # create_combinedJson_addCurrentPrice_fromAllFolders()
    # combinedData = os.path.join(basePath, 'results', 'combinedData_gpt.json')
    # filteredData = os.path.join(basePath, 'results', 'filteredData_gpt.json')
    # newCombinedData = merge_data(load_json(combinedData), load_json(filteredData))
    # write_readme(basePath, newCombinedData)
    # write_html(basePath, newCombinedData)
    
    # add current price in combinedData_gpt.json
    # combinedData_file = os.path.join(basePath, 'results', 'combinedData_gpt.json')
    # data = add_current_price(combinedData_file)
    # write_readme(basePath, data)
    
    
    
    
    
    
    
