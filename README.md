# cookStock
CookStock is a comprehensive stock screening tool implementing several advanced strategies to assist with stock analysis and selection. This tool can run in batch mode, automating the screening and analysis process using data from the YahooFinance API.

# Key Features

1. Filters stocks according to Mark Minervini's stage 2 criteria, including moving average, volume, and price position strategies.

2. Detects volatility contraction patterns, including identifying potential pivots, assessing for deep corrections, and evaluating selling pressure to determine if it has dried up.
Rule #1 Stock Valuation Tool:

3. Calculates each stock's intrinsic value based on the Rule #1 investing principles, allowing comparison to the stock's market price.

4. Retrieves the latest news on stocks to stay updated with relevant events that might affect stock performance.
Use YahooFinance API to pull stock data for screening,

all the tools can run under a batch mode, which allows you to screen and analyze stocks automatically

# Data Source and Automation
Using the YahooFinance API, cookStock pulls stock data automatically for analysis. All tools are designed to run in batch mode, enabling automatic daily screening of stocks based on the selected criteria.

Here is an example of TSLA's volatility contraction pattern
![Figure_1](https://user-images.githubusercontent.com/25359807/114505746-b0be2700-9be5-11eb-9347-dbcc2351158f.png)

Usage Instructions
1. Run cookStockPipeline.py to perform both stage 2 template screening and apply contraction pattern detection on the selected stocks.
2. Run runBatch_cookStock_stage2template.py to filter stocks meeting stage 2 template criteria.
3. Run runBatch_volatility_contraction_pattern.py to identify stocks with a defined contraction pattern.

We also run the selection daily and post here:
[View Daily Selection Results](./results/README.md)

If you enjoy this project and even gain profits from it, consider supporting through a donation via PayPa

| **Paypal** |
|------------|
| [![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/paypalme/JJandSean/10/?locale.x=en_US&currency_code=USD) |
