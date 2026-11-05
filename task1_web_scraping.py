import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt

def scrape_headlines(rss_url):
    """Scrapes headlines from an RSS news feed."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(rss_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    items = soup.find_all("item")
    headlines = []
    for item in items:
        title = item.title.text if item.title else ""
        if title:
            headlines.append(title)
    return headlines

def analyze_sentiment(headlines):
    """Analyzes sentiment polarity for each headline."""
    results = []
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    
    for title in headlines:
        analysis = TextBlob(title)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.05:
            sentiment = "Positive"
        elif polarity < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        sentiment_counts[sentiment] += 1
        results.append((title, polarity, sentiment))
        
    return results, sentiment_counts

def visualize_results(sentiment_counts):
    """Plots sentiment distribution as a bar chart."""
    labels = list(sentiment_counts.keys())
    counts = list(sentiment_counts.values())
    colors = ['#4CAF50', '#9E9E9E', '#F44336']
    
    plt.figure(figsize=(7, 5))
    plt.bar(labels, counts, color=colors)
    plt.title("News Headlines Sentiment Analysis")
    plt.xlabel("Sentiment Category")
    plt.ylabel("Number of Headlines")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # BBC World News RSS feed
    URL = "http://feeds.bbci.co.uk/news/world/rss.xml"
    print(f"Fetching headlines from {URL}...\n")
    
    titles = scrape_headlines(URL)
    print(f"Scraped {len(titles)} headlines.\n")
    
    analyzed, counts = analyze_sentiment(titles)
    
    # Display sample results
    print("--- Sample Headlines & Sentiments ---")
    for title, score, cat in analyzed[:5]:
        print(f"[{cat}] (Score: {score:+.2f}) -> {title}")
        
    print("\nSummary Counts:", counts)
    visualize_results(counts)