import os
import requests
import pandas as pd
from datetime import datetime
from openai import ChatCompletion
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def initialize_openai():
    ChatCompletion.api_key = OPENAI_API_KEY

def initialize_llama():
    return pipeline("text-classification", model="facebook/bart-large-mnli")

def fetch_news(api_url, query_params):
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def analyze_risk_with_gpt(content):
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in supply chain risk analysis."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error with OpenAI GPT: {e}")
        return None

def analyze_sentiment_with_llama(content, llama_pipeline):
    try:
        results = llama_pipeline(content)
        return results
    except Exception as e:
        print(f"Error with LLaMA: {e}")
        return None

def aggregate_data(news_data):
    try:
        structured_data = []
        for article in news_data['articles']:
            structured_data.append({
                "source": article['source']['name'],
                "title": article['title'],
                "description": article['description'],
                "content": article['content'],
                "published_at": article['publishedAt']
            })
        return pd.DataFrame(structured_data)
    except Exception as e:
        print(f"Error structuring data: {e}")
        return None

def main():
    initialize_openai()
    llama_pipeline = initialize_llama()

    news_api_url = "https://newsapi.org/v2/everything"
    query_params = {
        "q": "supply chain disruption",
        "from": datetime.now().strftime('%Y-%m-%d'),
        "sortBy": "relevance",
        "apiKey": NEWS_API_KEY
    }

    news_data = fetch_news(news_api_url, query_params)
    if not news_data:
        print("No data fetched.")
        return

    structured_data = aggregate_data(news_data)
    if structured_data is None:
        print("Error aggregating data.")
        return

    for _, row in structured_data.iterrows():
        print(f"Analyzing article: {row['title']}")
        gpt_analysis = analyze_risk_with_gpt(row['content'])
        print("\nRisk Analysis:")
        print(gpt_analysis)
        sentiment_analysis = analyze_sentiment_with_llama(row['content'], llama_pipeline)
        print("\nSentiment Analysis:")
        print(sentiment_analysis)
        print("\n---\n")

if __name__ == "__main__":
    main()
