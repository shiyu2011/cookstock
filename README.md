# cookStock

Implemente a handful of stock screening tools
1. Mark Minervini's stage 2 template searching (including moving average strategy, volume strategy and price position strategy)
2. Mark Minervini's volatility contraction pattern detection (including identifing patterns, if there is good pivot, if there is a deep correction and if selling pressure is dry)
3. Tool to calculate stock value based on RULE one principle (focus on value of each stock and compare it to sticker price)
4. Tool to extract news from YahooFinance

Use YahooFinance API to pull stock data for screening, 
all the tools can run under a batch mode, which allows you to screen and analyze stocks automatically

Here is an example of TSLA's volatility contraction pattern
![Figure_1](https://user-images.githubusercontent.com/25359807/114505746-b0be2700-9be5-11eb-9347-dbcc2351158f.png)

USAGE:
1. run cookStockPipeline.py to run both stage2 template selection and apply contraction pattern detection on selected stock
1. run runBatch_cookStock_stage2template.py to select stage2 stocks from all using template
2. run runBatch_volatility_contraction_pattern.py to select stocks with defined contraction pattern

We also run the selection daily and post here:
[View Daily Selection Results](./results/README.md)
