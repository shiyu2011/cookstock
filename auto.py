import json
import os

# Define paths
date_folder = "2024-11-13"
json_file = f"results/{date_folder}/Technology_HealthCare_BasicIndustries_ConsumerServices_Finance_Energy_ConsumerNon-Durables_ConsumerDurables.json"

with open(json_file) as f:
    data = json.load(f)

# Create README.md content
readme_content = f"# Stock Analysis for {date_folder}\n\n"
for stock_data in data["data"]:
    for ticker, details in stock_data.items():
        readme_content += f"- **{ticker}**\n"
        readme_content += f"  - Current Price: ${details['current price']}\n"
        readme_content += f"  - Support Price: ${details['support price']}\n"
        readme_content += f"  - Pressure Price: ${details['pressure price']}\n"
        readme_content += f"  - Good Pivot: {details['is_good_pivot']}\n"
        readme_content += f"  - Deep Correction: {details['is_deep_correction']}\n"
        readme_content += f"  - Demand Dry: {details['is_demand_dry']}\n"
        readme_content += f"  - ![Figure]({ticker}.jpg)\n\n"

# Write to README.md in the same folder as the JSON file
with open(f"results/{date_folder}/README.md", "w") as f:
    f.write(readme_content)

