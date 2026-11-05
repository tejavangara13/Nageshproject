import requests
from bs4 import BeautifulSoup
import re
import time
import sys

# Target demo e-commerce product
TARGET_URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
BUDGET_LIMIT = 55.00  # Target price threshold

def check_price(url):
    """Fetches product title and parses current price."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # Added timeout so it never hangs indefinitely
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract title and price
    title_elem = soup.find("h1")
    price_elem = soup.find("p", class_="price_color")
    
    if not title_elem or not price_elem:
        return "Unknown Product", None
        
    title = title_elem.get_text().strip()
    price_str = price_elem.get_text().strip()
    
    # Extract numerical price using regex
    price_match = re.search(r"[\d.]+", price_str)
    if price_match:
        price = float(price_match.group())
        return title, price
        
    return title, None

def send_notification(product_title, current_price, target_price):
    """Simulated notification alert."""
    print("\n" + "="*50, flush=True)
    print(" >>> PRICE DROP ALERT TRIGGERED! <<<", flush=True)
    print("="*50, flush=True)
    print(f"Product Name : {product_title}", flush=True)
    print(f"Current Price: £{current_price:.2f}", flush=True)
    print(f"Your Budget  : £{target_price:.2f}", flush=True)
    print(f"Product URL  : {TARGET_URL}", flush=True)
    print(" Status      : Alert notification successfully sent to user!", flush=True)
    print("="*50 + "\n", flush=True)

def monitor_price(url, budget, check_interval_seconds=5):
    """Monitors the price periodically."""
    print("--------------------------------------------------", flush=True)
    print(" Starting E-commerce Price Tracker...", flush=True)
    print(f" Target Limit : £{budget:.2f}", flush=True)
    print(f" Monitoring URL: {url}", flush=True)
    print("--------------------------------------------------\n", flush=True)

    attempts = 0
    while attempts < 3:  # Checks 3 times for demonstration
        attempts += 1
        try:
            timestamp = time.strftime('%H:%M:%S')
            print(f"[{timestamp}] Checking product price (Check #{attempts})...", flush=True)
            
            title, price = check_price(url)
            
            if price is not None:
                print(f"[{timestamp}] Product: '{title}' | Price: £{price:.2f}", flush=True)
                
                if price <= budget:
                    print(f" Deal Found! Current price (£{price:.2f}) is below budget (£{budget:.2f})!", flush=True)
                    send_notification(title, price, budget)
                    break  # Stop tracking after alerting
                else:
                    print(f" Price (£{price:.2f}) is above budget (£{budget:.2f}). Waiting...\n", flush=True)
            else:
                print(" Could not parse price from page.\n", flush=True)
                
        except Exception as e:
            print(f" Error checking page: {e}\n", flush=True)
            
        time.sleep(check_interval_seconds)

if __name__ == "__main__":
    monitor_price(TARGET_URL, budget=BUDGET_LIMIT, check_interval_seconds=3)