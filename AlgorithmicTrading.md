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

The `resample()` function is often used because it provides elaborate control and more flexibility on the frequency conversion of the time series. You can specify new time intervals, how to handle missing data and indicate how you want to resample the data. 

## Visualizing Time Series Data 

This task is simple to due to Pandas' plotting integration with Mathplotlib - we can just use the `plot()` function and pass the relevant arguments to it. 

```python 
import matplotlib.pyplot as plt

aapl['Close'].plot(grid=True)
plt.show()
```  

# Common Financial Analysis

From here on we can use `pandas` to dive into some of the common financial analyses that you can do so that you can actually start working towards developing a trading strategy. 

We will cover returns, moving windows, volatility calculation and Ordinary Least-Squares Regression (OLS). 


## Returns 

The simple daily percentage change doesn't take into account dividends and other factors. It represents the amount of percentage change in the value of a stock over a single day of trading. This value is easily calculated as there is a `pct_change()` function included in the Pandas package. 

```python 
import numpy as np

daily_close = aapl[['Adj Close']]
daily_pct_change = daily_close.pct_change()
```

Note that we calculate the log returns to get a better insight into the growth of the returns over time. 

Know how to calculate daily percentage change is nice but what about when you want to know the monthly or quarterly returns? Here, we can use the `resample()` function. 

```python 
# Resampling to business months - use last observation as value
monthly = aapl.resample('BM').apply(lambda x: x[-1])
# Monthly percentage change 
monthly.pct_change()
```

To do things manually without `pct_change()` we divide `daily_close` vlaues by the `daily_close.shift(1) - 1` value. 


The formula for calculating returns is as follows: 
```
daily_log_returns_shift = np.log(daily_close / daily_close.shift(1))
```

> r = p(t)/p(t-1) - 1

```python 
import matplotlib.pyplot as plt

daily_pct_change.hist(bins=50)
plt.show()
print(daily_pct_change.describe())
```

If we take a look at a usual distribution we will see that it is usually very symmetrical and normally distributed - the changes center around the bin 0.00. 

The `cumulative daily rate of return` is useful to determine the value of an investment at regular intervals. You can calculate the cumulative daily rate of return by using the daily percentage change values, adding `1` to them and calculating the cumulative product with the resulting values.  

`cumulative_daily_return = (1 + daily_pct_change).cumprod()` 

If we don't want to see the daily returns but rather the monthly returns - we can easily use the `resample()` function to bring the `cumulative_daily_return` to the montly level 

`cumulative_montly_return = cumulative_daily_return.resample("M").mean()`

This is simply for calculating returns but we will often see that these numbers do not mean much when we do not compare them to other stocks. In the following we will be comparing multiple stocks! 

First we need data - check out the code below where we get the stock data from Apple, Microsoft, IBM, and Google and store them in one big DataFrame 

```python 
def get(tickers, startdate, enddate): 
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    return(pd.concat(datas, keys=tickers,names=['Ticker','Date']))

tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']
all_data = get(tickers, datetime.datetime(2006, 10, 1), datetime.datetime(2021, 1, 1))
```

We can check out the plots for the daily percentage change using 

```python 
import matplotlib.pyplot as plt

daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')

daily_pct_change = daily_close_px.pct_change()

daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

plt.show()
```

Another interesting plot to check out is the scatter matrix. 

```python 
import matplotlib.pyplot as plt

pd.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1,figsize=(12,12))

plt.show()
```

In the arguments we specify that we want a Kernel Density Estimate (KDE) plot. This plot estimates the probability density function of a random variable. 


This concludes the first common financial analysis where we explore returns! Moving on to moving windows


## Moving Windows 

In moving windows, we compute the statistic on a window of data represented by a particular period of time and then slide that window by a specified interval. 

This rolling smoothes out short-term fluctuations and highlights longer-term trends in data. 

```python 
moving_avg = adj_close_px.rolling(window=40).mean()
```

We can plot out a couple of windows to see how it affects the data 

```python 
aapl['42'] = adj_close_px.rolling(window=40).mean()

aapl['252'] = adj_close_px.rolling(window=252).mean()

aapl[['Adj Close', '42', '252']].plot()

plt.show()
```

### Volatility Calculation 

The volatility of a stock is a measurement of the change in variance in the returns of a stock over a specific period of time. 

This is used to get a feel of the risk and we can compare it to other stocks. Generally the higher the volatility, the riskier the investment in the stock. 

The moving historical standard deviation of the log returns - ie the moving historical volatility - is of particular interest. 

```python
# rolling_std(data, window) * math.sqrt(window)
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)
```


As you will notice, the volatility is calculated by taking a rolling window standard deviation on the percentage change in a stock. 

Clearly changing the size of the window will change the overall result: a wider window will make the results less representative. If we make it smaller, then the results will come closer to the standard deviation. 


Thus, it is a skill to get the right window size based upon the data sampling frequency. 


## Ordinary Least-Squares Regression (OLS)

To perform this traditional regression analysis, we will be using the `statsmodels` library. 

```python 
import statsmodels.api as sm 
from pandas.core import datetools

all_adj_close = all_data[['Adj Close']]

all_returns = np.log(all_adj_close/all_adj_close.shift(1))

# Isolate AAPL returns
aapl_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'AAPL']
aapl_returns.index = aapl_returns.index.droplevel('Ticker')

# Isolate MSFT returns
msft_returns = all_returns.iloc[all)_returns.index.get_level_values('Ticker') == 'MSFT']
msft_returns.index = msft_returns.index.droplevel('Ticker)

# Build up dataframe
return_data = pd.concat([aapl_returns, msft_returns], axis=1)[1:]
return_data.columns = ['AAPL', 'MSFT']

X = sm.add_constant(return_data['AAPL'])

# Constructing the model
model = sm.OLS(return_data['MSFT'],X).fit()

print(model.summary())
```

These are data which aren't going deep into but here are some important information which we can also take into account: 

* `R-squared` is the coefficient of determination and indicates how well the regression line approximates the real data points 

* `Adj. R-squared` which is the adjusted R-squared value based on the number of observations and the degrees of freedom of the residuals 

* `F-statistic` measures how significant the fit is. It is calculated by dividing the mean squared error of the model by the mean squared error of the residuals

* `Prob (F-statistic)` indicates the probability that you wil lget the result of the `F-statistic` 

* `Log-likelihood` indicates the log of likelihood function 

* `AIC` is Akaike Information Criterion which adjusts the log-likelihood based on the number of observations and the complexity of the model 

* `BIC` is the Bayesian Information Criterion and is the same as AIC but penalizes models with more parameters more severely. 


## Building a Trading Strategy with Python 






