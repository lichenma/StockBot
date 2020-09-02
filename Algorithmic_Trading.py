import pandas_datareader as pdr
import datetime 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get(tickers, startdate, enddate): 
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    return(pd.concat(datas, keys=tickers,names=['Ticker','Date']))


aapl = get(['AAPL'], datetime.datetime(2006, 10, 1), datetime.datetime(2021, 1, 1))

short_window = 40
long_window = 100 

signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0

signals['short_mavg'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

signals['long_mavg'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

signals['positions'] = signals['signal'].diff()

print(signals)