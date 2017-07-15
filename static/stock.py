import numpy as np
from datetime import *
import requests
import quandl
import json
import re

quandl.ApiConfig.api_key = '2gUCuKixgquQbAYWb-uz'
alpha_vantage_key = 'BWH9ST7QEJE1LRQ7'
alpha_vantage_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval={}min&outputsize=compact&apikey={}'
yahoo_url = 'http://autoc.finance.yahoo.com/autoc?query={}&region=US&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback'


def get_data(ticker, dataset='WIKI', start_date='', end_date=''):
    ticker = ticker.upper()
    try:
        dataset = quandl.Dataset('{}/{}'.format(dataset, ticker))
        df = dataset.data(params={ 'start_date': start_date, 'end_date': end_date}).to_pandas()
        timestamps = []
        for time in df.index:
            timestamps.append(time.to_pydatetime() + timedelta(hours=9.5))
            timestamps.append(time.to_pydatetime() + timedelta(hours=16))
        prices = list(df[['Open', 'Close']].as_matrix().flatten())
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
        prices.append(float(costs['1. open']))
    return times, prices


def get_price_at_start_and_end_of_day(ticker):
    _, prices = get_intraday(ticker, 15)
    return float(prices[0]), float(prices[-1])


def get_price_change(ticker):
    start, end = get_price_at_start_and_end_of_day(ticker)
    return (end - start) / start


def get_name_from_ticker(ticker):
    req = requests.get(yahoo_url.format(ticker))
    for dic in json.loads(req.text[39:-2])['ResultSet']['Result']:
        if dic['symbol'] == ticker.upper():
            return(dic['name'])

stocks = {}


class User:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.user_stocks = {}  # Maps str ticker to UserStock purchased by user

    def buy_stock(self, ticker, purchase_date, purchase_quantity):
        ticker = ticker.upper()
        self.user_stocks[ticker] = UserStock(ticker, purchase_date, purchase_quantity)

class UserStock:

    def __init__(self, ticker, purchase_date, purchase_quantity):
        self.ticker = ticker
        self.purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
        self.purchase_quantity = purchase_quantity
        self.purchase_price = get_data(ticker, start_date=purchase_date)[1][0]
        self.name = get_name_from_ticker(ticker)

        if ticker in stocks:
            self.stock = stocks[ticker]
        else:
            stock = Stock(ticker)
            stocks[ticker] = stock
            self.stock = stock

        self._calc_max_and_min_prices()
        self.current_value = purchase_quantity * get_price_at_start_and_end_of_day(ticker)[1]

    def _calc_max_and_min_prices(self):

        timestamps, prices = self.stock.price_data['1Y']
        index = 0
        for i in range(len(timestamps)):
            if timestamps[i] > self.purchase_date:
                index = i
                break
        self.max_price = max(prices[index:])
        self.min_price = min(prices[index:])


class Stock:

    def __init__(self, ticker, category=''):

        self.ticker = ticker
        self.name = get_name_from_ticker(ticker)

        self.price_data = {
            '1d': get_intraday(ticker),
            '1w': get_history(ticker, 7),
            '1M': get_history(ticker, 30),
            '3M': get_history(ticker, 90),
            '6M': get_history(ticker, 183),
            '1Y': get_history(ticker, 365),
        }

        self.category = category

        self.description = ''

    def set_description(self, des):
        self.description = des
