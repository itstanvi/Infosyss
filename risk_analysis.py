import requests
import pandas as pd
from datetime import datetime
import openai  # Updated OpenAI import
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize OpenAI API and sentiment analysis pipeline
openai.api_key = OPENAI_API_KEY  # Updated for new API usage
llama_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")

# Function to fetch news
def fetch_news(query, api_key):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "from": "2025-01-01",  # You can set a static start date to ensure older articles are included
        "sortBy": "relevance",
        "language": "en",
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("News API Response:", response.json())  # Print the full response
        return response.json()
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

# Updated function to analyze risk with new OpenAI API
def analyze_risk(content):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Example model, adjust as per your preference
            prompt=f"Analyze the risk of the following text: {content}",
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].text.strip()  # Return the analyzed text
    except Exception as e:
        print(f"Error analyzing risk: {e}")
        return None

# Sentiment analysis using LLaMA
def analyze_sentiment(content):
    return llama_pipeline(content)

# Process fetched news data
def process_news_data(news_data):
    structured_data = []
    for article in news_data["articles"]:
        content = article["content"]
        risk_analysis = analyze_risk(content)
        sentiment_analysis = analyze_sentiment(content)
        structured_data.append({
            "title": article["title"],
            "description": article["description"],
            "content": content,
            "published_at": article["publishedAt"],
            "risk_analysis": risk_analysis,
            "sentiment": sentiment_analysis[0]["label"]
        })
    return pd.DataFrame(structured_data)

# Main function to execute the pipeline
def main():
    api_key = NEWS_API_KEY
    query = "chips"
    news_data = fetch_news(query, api_key)
    if news_data and "articles" in news_data:
        df = process_news_data(news_data)
        print(df)

if __name__ == "__main__":
    main()
