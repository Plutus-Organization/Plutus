import datetime

from flask import Flask, jsonify, render_template, request

from Plutus import stock

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


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
