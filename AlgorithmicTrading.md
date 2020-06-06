## Introduction 

Starting with an awesome guide written by Karlijin in [DataCamp](https://www.datacamp.com/community/tutorials/finance-python-trading) for context. 🙌


Technology has become a major asset in finance - the large data volumes along with the high rate and requency of financial transactions presents a perfect opportunity for technology to become the next big enabler. 

This introduction will focus on convering the basics that we need to get started 

- Stocks and trading strategies, what time series data is and what you need to set up a workspace 
- Introduction to time series data and some of the most common financial analyses such as moving windows, volatility calculation using the Python package Pandas 
- Development of a simple momentum strategy - step by step formulating and coding up a simple algorithmic trading strategy 
- Backtest the formulated trading strategy with Pandas, zipline and Quantopian 
- Optimizations to the strategy to make it perform better, and eventually evaluate the strategy's performance and robustness 


## Getting Started 

Before starting off with trading strategies, it is a good idea to get the hang of the basics first. \


### Stocks and Trading 

When companies want to grow and undertake new projects or expand, it can issue stocks to raise capital. Stock represents a share in the ownership of a company and is issued in return for money. Stocks are bought/sold and the price can move independently of a company's success. 

Bonds on the other hand is when companies raise money through borrowing, either as a loan from a bank or by issuing debt. 

To achieve a profitable return you will either go long or short in markets - you either buy shares thinking that the stock price will go up to sell at a higher price in the future or you sell your stock expecting that you can buy it back at a lower pice and realize a profit. When you follow a fixed plan to go long or short in markets then you have a trading strategy. 


Trading strategies are similar to building machine learning models: you formulate a strategy and specify it in a form that can be tested on your computer, do some preliminary testing or backtesting, optimize the strategy, and lastly evaluate the performance and robustness of the strategy. 


Trading strategies are usually verified by backtesting - you reconstruct using historical data, trades that would have occurred in the past given by the strategy that you have developed. This way you can gauge the effectiveness of the strategy and use it as a starting point to optimize and improve the strategy before applying it to the real markets. This relies however, on the belief that any strategy that has worked out well in the past will also work out well in the future - and the adverse. 

### Time Series Data 

A time series is a sequence of numerical data points taken a successive equally spaced points in time. In investing, a time series tracks the movement of the chosen datapoints such as stock prices over a specified period of time with data points recorded at regular intervals. 


### Setting up the Workspace 

Anaconda is a high-performance distribution of Python and R and includes over 100 of the most popular Python, R and Scala packages for data science. 

When using Python for finance you will often also find yourself using the data manipulation package, Pandas. Other packages such as NumPy, SciPy, Matplotlib will also pop up as you start digging deeper. 

Let's start with Pandas and use it to analyze time series data. 


### Pandas 






