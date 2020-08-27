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

The `pandas-datareader` package allows for reading in data from sources such as Google, World Bank, etc. 

```python 
import pandas_datareader as pdr 
import datetime 
aapl  = pdr.get_data_yahoo('AAPL', 
                            start=datetime.datetime(2006,10,1),
                            end=datetime.datetime(2012,1,1))
```


There is also the Quandl library which allows you to get data from Google Finance. 

```python 
import quandl 
appl = quandl.get("WIKI/APPL", start_date="2006-10-01", end_date="2012-01-01")
```


### Working With Time Series Data

We start by using `pandas_datareader` to import data into the workspace. The resulting object `aapl` is a DataFrame - a 2-dimensional labeled data structure with columns of potentially different types. Given a DataFrame we can run the `head()` and `tail()` functions to take a peek at the first and the last rows of the DataFrame. 


The data returned from `pandas-datareader` contains six columns - high, low, open, close, volumn, adj Close. 

High and low are used to give the extreme price points for the stock each day. Open and close give the price points at the beginning and the end of the day. Volumne is used to register the number of shares that got traded during a single day. Adj Close is the `adjusted closing price` - the closing prices of the day that has been slightly adapted to include any actions that occurred at any time before the next day's open. 



Tip: We can now save this data to a csv file with the `to_csv()` function from `pandas` and us the `read_csv()` function to read data back into Python. This is extremely handy in cases where, for example, the Yahoo API endpoint has changed and you don't have access to your data any longer 

```Python
import pandas as pd 
appl.to_csv('data/appl_ohlc.csv')
df = pd.read_csv('data/aapl_chlc.csv', header=0, index_col='Date', parse_dates=True)
```

Now that we have briefly inspected the first lines of the data and taken a look at some summary statistics, its time to go a little deeper. 

One way to do this is to inspect the index and the columns and by selecting a small subset of the data. By subsetting, we get a one-dimensional labeled array that is capable of holding any type. Recall that the original DataFrame structure was a two-dimensional labeled array with columns that potentially hold different types of data. 

```Python
aapl.index 
aapl.columns
```

For example, we can subset the `Close` column by selecting the last 10 values of the Dataframe - use the square brackets `[]` to isolate the last ten values. This looks something like this `aapl['Close'][-10:]` and returns a `Series` - the one dimensional array that is capable of holding any type. 


The square brackets can be useful to subset the data but they are maybe not the most idiomatic way to do things with Pandas. One alternate way of handling things is using the `loc()` and `iloc()` functions: the former is used for label-based indexing and the latter is used for positional indexing. 

In practice, this means that you can pass the label of the row labels, such as `2007` and `2016-11-01`, to the `loc()` function, while you pass integers such as `22` and `43` to the `iloc()` function. 

We can sample rows from the dataset using `sample()` and use `resample()` to take a look at the data from a monthly level instead of daily. 

The `resample()` 






