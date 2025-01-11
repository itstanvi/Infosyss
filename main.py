from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = "c2326b45d9bd45caba2e2e4866c6844a" 

def fetch_news(query, from_date, to_date):
    api_url = "https://newsapi.org/v2/everything"
    query_params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "sortBy": "relevance",
        "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/fetch-news', methods=['GET'])
def get_news():
    query = request.args.get('query', 'supply chain')
    from_date = request.args.get('from', '2023-01-01')
    to_date = request.args.get('to', '2023-12-31')
    
    news_data = fetch_news(query, from_date, to_date)
    return jsonify(news_data)

if __name__ == '__main__':
    app.run(debug=True)
