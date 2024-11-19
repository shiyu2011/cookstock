import json
import os
import sys
import datetime as dt


class CookStockUtils:
    def __init__(self):
        self.basePath = self.find_path()

    def find_path(self):
        """Find the base path of the 'cookstock' directory."""
        home_dir = os.path.expanduser("~")
        for root, dirs, files in os.walk(home_dir):
            if 'cookstock' in dirs:
                return os.path.join(root, 'cookstock')
        return None

    def read_json(self, file_path):
        """Read a JSON file and return its content."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def save_json(self, data, file_path):
        """Save data to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"JSON saved to '{file_path}'")

    def check_current_price_from_raw_selections(self, folder_name, json_file_name, output_file_name):
        """Prepare JSON data by updating the current price and change percentage."""
        folder = os.path.join(self.basePath, 'results', folder_name)
        file_path = os.path.join(folder, json_file_name)
        data = self.read_json(file_path)

        for entry in data["data"]:
            for ticker, details in entry.items():
                print(f"Processing ticker: {ticker}")
                x = cookFinancials(ticker)
                s = x.get_current_price()
                current_price_in_data = float(details['current price'])
                details['current price at check'] = s
                details['change'] = (s - current_price_in_data) / current_price_in_data
                #add check time
                details['time at Check'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Updated {ticker}: Current Price: {s}, Change: {details['change']:.4%}")

        # Sort data based on change percentage
        data["data"].sort(key=lambda x: list(x.values())[0]['change'], reverse=True)

        # Save the updated JSON
        output_file = os.path.join(self.basePath, 'tmp', output_file_name)
        self.save_json(data, output_file)
        
    def order_tickes_by_change_only(self, full_folder_path , json_file_name, output_file_name):
        """Order tickers based on the change percentage."""
        file_path = os.path.join(full_folder_path, json_file_name)
        data = self.read_json(file_path)

        data["data"].sort(key=lambda x: list(x.values())[0]['change'], reverse=True)
        file_path = os.path.join(full_folder_path, 'tmp', output_file_name)    
        self.save_json(data, file_path)

    def remove_duplicates_and_generate_readme(self, combined_file_name, readme_file_name):
        """Remove duplicates from combined JSON and generate a README."""
        file_path = os.path.join(self.basePath, 'results', combined_file_name)
        data = self.read_json(file_path)

        unique_data = {"data": []}
        unique_tickers = []

        for entry in data["data"]:
            for ticker, details in entry.items():
                if ticker not in unique_tickers:
                    unique_tickers.append(ticker)
                    unique_data["data"].append({ticker: details})
                else:
                    for unique_entry in unique_data["data"]:
                        for unique_ticker, unique_details in unique_entry.items():
                            if unique_ticker == ticker and unique_details['date of the selection'] == details['date of the selection']:
                                print(f"Duplicate ticker {ticker} with the same date {details['date of the selection']} removed.")
                            elif unique_ticker == ticker:
                                unique_data["data"].append({ticker: details})
                                unique_tickers.append(ticker)

        self.save_json(unique_data, file_path)

        # Generate README content
        readme_content = "# Daily Stock Analysis\n\n"
        readme_content += "This report provides an overview of selected stocks with volatility contraction patterns and analysis details.\n\n"
        readme_content += "## Stocks Overview\n\n"

        for entry in unique_data["data"]:
            for ticker, details in entry.items():
                readme_content += f"### {ticker}\n"
                readme_content += f"- **Current Price during run time**: {details['current price']}\n"
                readme_content += f"- **Support Price**: {details['support price']}\n"
                readme_content += f"- **Pressure Price**: {details['pressure price']}\n"
                readme_content += f"- **Good Pivot**: {details['is_good_pivot']}\n"
                readme_content += f"- **Deep Correction**: {details['is_deep_correction']}\n"
                readme_content += f"- **Demand Dry**: {details['is_demand_dry']}\n"
                readme_content += f"- **Current Price at Check**: {details['current price at Check']}\n"
                readme_content += f"- **Price Change**: {details['price_change']:.4%}\n"
                readme_content += f"- **Date of the Selection**: {details['date of the selection']}\n"
                readme_content += f"- **Time at Check**: {details['time at Check']}\n"
                if 'fig' in details:
                    fig_path = details['fig']
                    img_path = os.path.relpath(fig_path, start=os.path.join(self.basePath, 'results'))
                    readme_content += f"![{ticker} Chart](./{img_path})\n"
                readme_content += "\n"

        readme_file = os.path.join(self.basePath, 'results', readme_file_name)
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        print(f"README file written to '{readme_file}'")

    def count_tickers(self, json_file):
        """Count the total number of entries in a JSON file."""
        data = self.read_json(json_file)
        #get all keys for each entry
        tickers = [list(entry.keys())[0] for entry in data["data"]]
        print(f'Total tickers: {len(tickers)}')
        unique_tickers = list(set(tickers))
        print(f'Unique tickers: {len(unique_tickers)}')
        return len(tickers)
    
    def count_ticker_with_review(self, json_file):
        """Count the total number of entries with news reviews in a JSON file."""
        data = self.read_json(json_file)
        count = 0
        for entry in data["data"]:  # Iterate through the list of entries
            for ticker, details in entry.items():  # Each ticker (e.g., "MRBK") is a key
                news = details.get("news", [])  # Get the "news" field (default to an empty list)
                if isinstance(news, list):  # Ensure "news" is a list
                    # Check if any news item contains a "review"
                    for news_item in news:
                        if "review" in news_item:
                            print(f'Ticker: {ticker}, Review: {news_item["review"]}')
                            count += 1
                            break  # Count the ticker once, even if it has multiple reviews
        return count
    
    def check_if_duplicates(self, json_file):
        """Check if there are any duplicate entries in a JSON file."""
        data = self.read_json(json_file)
        tickers = [list(entry.keys())[0] for entry in data["data"]]
        unique_tickers = list(set(tickers))
        return len(tickers) != len(unique_tickers)
    
    
    def check_and_remove_duplicates(self, json_file):
        print(f"is duplicate: {self.check_if_duplicates(json_file)}")
        print(f"total tickers: {self.count_tickers(json_file)}")
        print(f"start removing duplicates")
        
        # Read data from the JSON file
        data = self.read_json(json_file)

        # Keep track of seen tickers
        seen_tickers = set()
        unique_data = []

        # Iterate over entries and add only unique tickers to the new list
        for entry in data["data"]:
            for ticker, _ in entry.items():
                if ticker not in seen_tickers:
                    unique_data.append(entry)
                    seen_tickers.add(ticker)

        # Replace the original data with the unique entries
        data["data"] = unique_data

        # Save the updated data back to the JSON file
        self.save_json(data, json_file)
        print(f"end removing duplicates")
        print(f"total tickers after removing duplicates: {self.count_tickers(json_file)}")
        print(f"is duplicate after removing duplicates: {self.check_if_duplicates(json_file)}")

    def convert_json_to_html(self, json_file, output_html_file):
        """
        Converts a JSON file containing stock data to an HTML file with a table and embedded images.
        Args:
            json_file (str): Path to the JSON file.
            output_html_file (str): Path where the generated HTML file will be saved.
        """
        # Load JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Start generating HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Stock Analysis</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 10px;
                    text-align: center;
                }
                th {
                    background-color: #f4f4f4;
                }
                img {
                    max-width: 300px; /* Increased maximum width */
                    height: auto;
                }
            </style>
        </head>
        <body>
            <h1>Daily Stock Analysis</h1>
            <table>
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Current Price</th>
                        <th>Support Price</th>
                        <th>Pressure Price</th>
                        <th>Good Pivot</th>
                        <th>Deep Correction</th>
                        <th>Demand Dry</th>
                        <th>Figure</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Generate rows for the table
        for entry in data["data"]:
            for ticker, details in entry.items():
                fig_path = details.get("fig", "")
                img_relative_path = os.path.relpath(fig_path, start=os.path.dirname(output_html_file)) if fig_path else "No image"
                html_content += f"""
                <tr>
                    <td>{ticker}</td>
                    <td>{details['current price']}</td>
                    <td>{details['support price']}</td>
                    <td>{details['pressure price']}</td>
                    <td>{details['is_good_pivot']}</td>
                    <td>{details['is_deep_correction']}</td>
                    <td>{details['is_demand_dry']}</td>
                    <td><img src="{img_relative_path}" alt="{ticker} Figure"></td>
                </tr>
                """

        # Close the HTML structure
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Save the HTML content to a file
        with open(output_html_file, 'w') as f:
            f.write(html_content)
        print(f"HTML file generated at: {output_html_file}")

# Example usage
if __name__ == "__main__":
    util = CookStockUtils()

   # Check current price from raw selections
    # util.check_current_price_from_raw_selections('2024-11-14', 'Technology_HealthCare_BasicIndustries_ConsumerServices_Finance_Energy_ConsumerNon-Durables_ConsumerDurables.json', 'updated_data.json')

    # Order tickers by change percentage
    # util.order_tickes_by_change_only('/home/user/cookstock/results', 'combinedData.json', 'ordered_data.json')

    # Remove duplicates and generate README
    # util.remove_duplicates_and_generate_readme('combinedData.json', 'README.md')
    file = os.path.join(util.basePath, 'results', 'combinedData_gpt.json')
    print(util.count_tickers(file))
    print(util.check_if_duplicates(file))
    util.check_and_remove_duplicates(file)
    
    print(util.count_ticker_with_review(file))
