from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

# Load user and portfolio data from a JSON file
with open('stock.json', 'r') as file:
    user_data = json.load(file)

api_key = "KABTICZOTHQMZ7GP"  # Replace with your actual AlphaVantage API key

# Function to fetch daily time series stock information
def get_daily_time_series(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Will raise an exception for HTTP errors
        data = response.json()
        # Adjust the key based on the actual structure of the API response
        return data.get("Time Series (Daily)")
    except requests.exceptions.RequestException as e:
        print(f"Request for ticker {ticker} failed: {e}")
        return None

@app.route('/')
def home():
    portfolios = user_data.get('portfolios', [])
    # Fetch stock details for each item in the portfolios
    for portfolio in portfolios:
        for item in portfolio['items']:
            ticker = item['ticker']
            # Be careful with API rate limits when fetching details
            item['details'] = get_daily_time_series(ticker) or {}
    return render_template('index.html', user_data=user_data, portfolios=portfolios)

if __name__ == '__main__':
    app.run(debug=True)
