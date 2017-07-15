import matplotlib.pyplot as plt
import numpy as np
from datetime import *
import requests
import quandl
import json
import re

quandl.ApiConfig.api_key = '2gUCuKixgquQbAYWb-uz'
alpha_vantage_key = 'BWH9ST7QEJE1LRQ7'
alpha_vantage_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval={}min&outputsize=compact&apikey={}'


def get_data(ticker, dataset='WIKI', start_date='', end_date=''):
    ticker = ticker.upper()
    try:
        dataset = quandl.Dataset('{}/{}'.format(dataset, ticker))
        df = dataset.data(params={ 'start_date': start_date, 'end_date': end_date}).to_pandas()
        timestamps = []
        for time in df.index:
            timestamps.append(time.to_pydatetime() + timedelta(hours=9.5))
            timestamps.append(time.to_pydatetime() + timedelta(hours=16))
        prices = df[['Open', 'Close']].as_matrix().flatten()
        return timestamps, prices
    except Exception as e:
        return None


def get_history(ticker, days):
    """Queries quandl API for stock data.
    
    :param str ticker: Stock ticker code.
    :param int days: Number of days since today.
    :returns: 2D array of open and closing costs.
    :rtype: np.array
    """
    now = datetime.today()
    start = (now - timedelta(days=days)).strftime('%Y-%m-%d')
    return get_data(ticker, start_date=start)


def get_intraday(ticker, interval=5):
    req = requests.get(alpha_vantage_url.format(ticker, interval, alpha_vantage_key))
    text = json.loads(req.text)['Time Series ({}min)'.format(interval)]
    times = []
    prices = []
    
    now = datetime(2017, 7, 15)  # TFW your date is hardcoded
    for time, costs in sorted(text.items()):
        current = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if now - current > timedelta(days=1):
            continue
        times.append(current)
        prices.append(costs['1. open'])
    return times, prices


def get_price_change(ticker):
    _, prices = get_intraday('AAPL', 15)
    return (float(prices[-1]) - float(prices[0])) / float(prices[0])



