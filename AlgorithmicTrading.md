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

### Common Trading Strategies 

Recall that trading strategies are fixed plans to go long or short in markets. In general there are two common trading strategies - `momentum strategy` and `reversion strategy`. 

Momentum strategy is also known as divergence or trend trading. when you follow this strategy you do so believing that the movement of a quantity will continue in its current direction. You trust that stocks have momentum upward or downwards that you can detect and exploit. 

Examples include moving average crossover, dual moving average crossover and turtle trading. 

* Moving average crossover is when price of an asset moves from one side of a moving average to the other. This crossing over indicates a change in momentum and is used as a point of making the decision to enter or exit the market. We will be coming this strategy which is the "hello world" of quantitative trading later in this tutorial

* Dual moving average crossover is when a short-term average crosses a long-term average. This signal identifies that the momentum is shifting in the direction of the short-term average. Buy signal is generaged when the short-term average crosses the long-term average and rises above it and vice versa

* Turtle trading was a popular trend taught by Richard Dennis which is to buy futures on a 20-day high and sell on a 20-day low. 



On the other hand, the `reversion strategy`, also known as convergence or cycle trading centers around the belief that the movement of a quantity will eventually reverse. Examples include the mean reversion strategy and pairs trading mean-reversion

* Mean reversion strategy centers around the idea that stocks return to their mean and you can exploit when it deviates from that mean 

* Pairs trading mean-reversion states that if two stocks can be identified that have a relatively high correlation, the change in the difference in price between the two stocks can be used to signal trading events if one of the two moves out of correlation with the other. In this case the stock with the higher price is considered to be in the short position - it should be sold since the higher-priced stock will return to the mean. The lower priced stock is considered to be in the long position as the price is expected to rise as the correlation returns to normal 



Aside from these two main strategies, there are also other ones which come up every once in a while. One example is the forecasting strategy which attempts to predict the direction or value of a stock in subsequent future time periods based on certain historical factors. There is also High-Frequency Trading(HFT) strategy which exploits the sub-millisecond market microstructure. 

## Simple Trading Strategy

We will be starting off with the "hello world" of quantitative trading - moving average crossover. We will create two separate Simple Moving Averages (SMA) of a time series with different lookback periods (ex 40 days and 100 days). If the short moving average exceeds the long moving average then we go long - if the long moving average exceeds the short moving average then we exit. 


We will create the set of short and long moving averages using the `rolling()` function to start the rolling window calculations. 

This value will be stored in a `signals` DataFrame. 

After the averages have been calculated and stored - we need to generate a buy or sell signal when the short moving average crosses the long moving average. 

```python 

short_window = 40
long_window = 100 

signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0

signals['short_mavg'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

signals['long_mavg'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

signals['signal'][short_window:] = np.where(signals['short_mvag'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

signals['positions'] = signals['signal'].diff()

print(signals)
```

## Backtesting the Trading Strategy

With our strategy at hand, we will go ahead and backtest it and calculate its performance. 

### Backtesting Pitfalls 

Backtesting consists of testing a trading strategy on relevant historical data to make sure that it is an actual viable strategy before starting to make any moves. There are some pitfalls to keep in mind however. 

* External events such as market regime shifts, regulatory changes, macroeconomic events 

* Liquidity constraints such as the ban of short sales

* Personal bias, for example, overfitting a model (optimization bias), ignoring a strategy rules because you want to (interference), introducing information into past data (lookahead bias)

### Backtesting Components 

There are four main components present in every backtester: 

* Data handler, interface to a set of data 

* Strategy, which generates a signal to go long or short based on data

* Portfolio, which generates orders and managers Profit and Loss 

* Execution handler, which sends the order to the broker and receives the signals that the stock has been bought or sold 

### Implementation of a Simple Backtester 

First we will be manually setting up a backtesting visualization using `matplotlib`. 

```python 
initial_capital = float(100000.0)

positions = pd.DataFrame(index=signals.index).fillna(0.0)

positions['AAPL'] = 100*signals['signal']

portfolio = positions.multiply(aapl['Adj Close'], axis=0)

pos_diff = positions.diff()

portfolio['holdings'] = (positions.multiply(aapl['Adj Close'], axis=0)).sum(axis=1)

portfolio['cash' = initial_capital - (pos_diff.multiply(aapl['Adj Close'], axis=0)).sum(axis=1).cumsum()

portfolio['total'] = portfolio['cash'] + portfolio['holdings']

portfolio['returns'] = portfolio['total'].pct_change()

print(portfolio.head())
```

We can now visualize this using Matplotlib

```python 
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index, 
        portfolio.total[signals.positions == 1.0],
        '^', markersize=10, color='m')
ax1.plot(portfolio.loc[signals.positions == -1.0].index, 
        portfolio.total[signals.positions == -1.0], 
        'v', markersize=10, color='k')

plt.show()
```

### Backtests with Zipline & Quantopian 

Quantopian is a free community-centered hosted platform for building and executing trading strategies. It is powered by `zipline`, a Python library for algorithmic trading. 

When we create a "New Algorithm" you will see that we have two definitions to start working from - `initialize()` and `handle_data()`. 

The first function is called when the program is started and perfroms one-time startup logic. As an argument, the `initialize()` function takes a context used to store state during a backtest or live trading. 

The `handle_data()` function is called once a minute during simulation or live-trading to decide what orders if any, should be placed per minute. The function takes in context and data as the input parameters - context is the same as outlined above while data is an object that stores several API functions (ex. `current()` to retrieve the most recent value of a given field or `history()` to get trailing windows of historical pricing)

Another object present in quantopian is `portfolio` which stores information about the porfolio. 

The `order_target()` is used to place an order to adjust a position to a target number of shares. Placing a negative target will result in a short position. 

Once the strategy has been implemented we have the option to `Run Full Backtest` which allows us to easily backtest our algorithm on historical data. 


Here is the sample algorithm from this tutorial: 

```python 
def initialize(context):
    context.sym = symbol('AAPL')
    context.i = 0


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.sym, 'price', 100, '1d').mean()
    long_mavg = data.history(context.sym, 'price', 300, '1d').mean()

    # Trading logic
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.sym, 100)
    elif short_mavg < long_mavg:
        order_target(context.sym, 0)

    # Save values for later inspection
    record(AAPL=data.current(context.sym, "price"),
           short_mavg=short_mavg,
           long_mavg=long_mavg)
```

## Improving the Trading Strategy 

There are several algorithms which can be used to improve a model on a continuous basis such as KMeans, k-Nearest Neighbors (KNN), Classification or Regression Trees and the Genetic Algorithm. 

We won't be covering these topics in this tutorial but these are good topics to look into to improve the base algorithm! 


## Evaluating Moving Average Crossover Strategy 

Aside from improving the strategy we should also be able to calculate some metrics to further judge our algorithm. First of all we can make use of the `Sharpe ratio` to get to know whether the portfolio's returns are the result of the fact that you decided to make smart investments or to take a lot of risks. 

The ideal case is that the returns are considerable but the additional risk of investing is as small as possible. The greater the portfolio's Sharpe ratio, the better: a ratio greater than 1 is acceptable, 2 is very good and 3 is excellent. 

```python
# annualized Sharpe ratio
sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
```

The Sharpe ratio is usually not considered as a standalone and is usually compared to other stocks. The best way to approach this issue is to extend the original trading strategy to other stocks. 

There is also `Maximum Drawdown` which measures the largest single drop from peak to bottom in the value of a portfolio. 

```python 
# Define a trailing 252 trading day window 
window = 252

rolling_max = aapl['Adj Close'].rolling(window, min_periods=1).max()
daily_drawdown = aapl['Adj Close']/rolling_max - 1.0

max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()
```

Finally we will go over the Compound Annual Growth Rate (CAGR), which provides us with a constant rate of return over the time period. The rate is determined by dividing the investments ending value (EV) by the investment's beginning value (BV). You raise the result to the power of 1/n, where n is the number of periods. We take 1 from the consequent result and we have our value: 

```
(EV/BV)^1/n - 1
```

There are so many other metrics to consider but this is all that we will be going over in this introduction. 

This concludes the tutorial! 