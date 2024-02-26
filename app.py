from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

with open('stock.json', 'r') as file:
    user_data = json.load(file)

api_key = "KABTICZOTHQMZ7GP"

def get_daily_time_series(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  

        data = response.json()  
        return data

    except requests.exceptions.RequestException as e:
        print(f"Request for ticker {ticker} failed: {e}")
        return None

@app.route('/')
def homepage():  
    ticker_and_quantity_dict = {}
    for portfolio in user_data.get('portfolios', []):
        for item in portfolio['items']:
            ticker_and_quantity_dict[item['ticker']] = item['quantity']

    return jsonify(ticker_and_quantity_dict)

@app.route('/api/portfolios')
def api_portfolios():
    portfolios = user_data.get('portfolios', [])
    for portfolio in portfolios:
        for item in portfolio['items']:
            ticker = item['ticker']
            quantity = item['quantity']
            item['details'] = {
                "daily_time_series": get_daily_time_series(ticker) or {},
                "quantity": quantity
            }
    return jsonify(portfolios)


if __name__ == '__main__':
    app.run(debug=True)

#curl http://localhost:5000/
#curl http://localhost:5000/api/portfolios