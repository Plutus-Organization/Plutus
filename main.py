from flask import Flask, jsonify, render_template, request

from static import stock
from static.articles import *

app = Flask(__name__)
article_source_manager = RelevantArticlesSource(2)

user = stock.User('name', 'email')
user.buy_stock('TSLA', '2017-02-10', 10)
user.buy_stock('MSFT', '2017-02-10', 10)

stock.stocks = {
    'AAPL': stock.Stock('AAPL', 'tech'),
    'GOOG': stock.Stock('GOOG', 'tech'),
    'MSFT': stock.Stock('MSFT', 'tech'),
    'TSLA': stock.Stock('TSLA', 'tech'),
    'XON': stock.Stock('XON', 'energy')
}

@app.route('/get_history', methods=['GET', 'POST'])
def get_history():

    ticker = request.args.get('ticker')
    days = int(request.args.get('days', ''))

    timestamps, prices = stock.get_history(ticker, days)
    timestamps = [time.strftime('%Y-%m-%d %H:%M:%S') for time in timestamps]
    prices = list(prices)
    return jsonify(timestamps=timestamps, prices=prices)


@app.route('/get_article_from_name', methods=['GET'])
def get_article_for_stock_name():
    stock_name = request.args.get('name')
    article = article_source_manager.retrieve_topmost_article(stock_name.lower())
    article_source_manager.add_article_to_db(article)
    return jsonify(url=article.article_url, summary=article.article_summary)


@app.route('/get_intraday', methods=['GET', 'POST'])
def get_intraday():

    ticker = request.args.get('ticker')

    timestamps, prices = stock.get_intraday(ticker)
    timestamps = [time.strftime('%Y-%m-%d %H:%M:%S') for time in timestamps]
    prices = list(prices)
    return jsonify(timestamps=timestamps, prices=prices)


@app.route('/get_user_stocks', methods=['GET', 'POST'])
def get_user_stocks():
    stocks = []
    for stock in user.user_stocks.values():
        stock_data = {}
        stock_data['ticker'] = stock.ticker
        stock_data['purchase_date'] = stock.purchase_date
        stock_data['name'] = stock.name
        stock_data['current_value'] = stock.current_value
        stock_data['min_price'] = stock.min_price
        stock_data['max_price'] = stock.max_price
        stock_data['purchase_quantity'] = stock.purchase_quantity
        stocks.append(stock_data)

    return jsonify(stocks=stocks)

@app.route('/get_stocks', methods=['GET', 'POST'])
def get_stocks():
    stocks = []
    for s in stock.stocks.values():
        stock_data = {}
        stock_data['ticker'] = s.ticker
        stock_data['name'] = s.name
        stock_data['price_data'] = s.price_data
        stock_data['category'] = s.category
        stocks.append(stock_data)

    return jsonify(stocks=stocks)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
