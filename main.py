import datetime

from flask import Flask, jsonify, render_template, request

import stock

app = Flask(__name__)


@app.route('/stock/get_data')
def get_data():
    req = request.json
    ticker = req['ticker']
    start_date = req.get('start_date', '')
    end_date = req.get('end_date', '')

    timestamps, prices = stock.get_data(ticker, start_date, end_date)
    timestamps = [time.strftime('%Y-%m-%d %H:%M:%S') for time in timestamps]
    prices = list(prices)
    return jsonify(timestamps=timestamps, prices=prices)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
