import datetime

from flask import Flask, jsonify, render_template, request

from static import stock
from articles import *

app = Flask(__name__)


@app.route('/get_history', methods=['POST'])
def get_history():

    ticker = request.args.get('ticker')
    days = int(request.args.get('days', ''))

    print(ticker, days, 'FUCKK')

    timestamps, prices = stock.get_history(ticker, days)
    timestamps = [time.strftime('%Y-%m-%d %H:%M:%S') for time in timestamps]
    prices = list(prices)
    return jsonify(timestamps=timestamps, prices=prices)


@app.route('/get_article_from_name', methods=['GET'])
def get_article_for_stock_name():
    stock_name = request.args.get('name')
    article_source_manager = RelevantArticlesSource(2)
    article = article_source_manager.retrieve_topmost_article(stock_name.lower())
    article_source_manager.add_article_to_db(article)
    return jsonify(url=article.article_url, summary=article.article_summary)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
