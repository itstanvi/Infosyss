from flask import Flask, request, jsonify
import requests
import os


NEWS_API_KEY = "c2326b45d9bd45caba2e2e4866c6844a"


app = Flask(__name__)


NEWS_API_URL = "https://newsapi.org/v2/everything"

@app.route('/fetch-news', methods=['GET'])
def fetch_news():

    keyword = request.args.get('keyword', 'chips')  # Default keyword: chips
    from_date = request.args.get('from', '2025-01-01')  # Default from date
    to_date = request.args.get('to', '2025-01-25')  # Default to date


    params = {
        "q": keyword,
        "from": from_date,
        "to": to_date,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)


    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch news", "status_code": response.status_code}), 500

if __name__ == "__main__":
    app.run(debug=True)
