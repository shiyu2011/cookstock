import os
import sys
import datetime as dt
import json

def find_path():
        home_dir = os.path.expanduser("~")  # Get the home directory
        for root, dirs, files in os.walk(home_dir):  # Walk through the directory structure
            if 'cookstock' in dirs:
                return os.path.join(root, 'cookstock')
        return None  # Return None if the folder was not found
    
#set cookstock path
basePath = os.path.join(find_path())
srcPath = os.path.join(basePath, 'src')
sys.path.insert(0, srcPath)

from cook_stock_utils import CookStockUtils
tool = CookStockUtils()

# tool.check_current_price_from_raw_selections('2024-11-15', 'Technology_HealthCare_Finance_Energy.json', 'current_price_11_15.json')
file = os.path.join(basePath, 'results', '2024-11-15', 'Technology_HealthCare_Finance_Energy.json')
outHtml = os.path.join(basePath, 'tmp', 'current_price_11_15.html')
tool.convert_json_to_html(file, outHtml)
# tool.order_tickes_by_change_only('/home/rxm/cookstock/', 'tmp.json', 'reorder_11_14.json')