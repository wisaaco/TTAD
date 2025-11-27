#!/usr/bin/env python3
"""
Example script to fetch prices from the simulator and save to CSV
This is a starting point - students should modify and improve this script
"""

import requests

# URL of the price simulator (use container name when running inside Docker)
SIMULATOR_URL = "http://price-simulator:8088"
# For testing outside container, use: "http://localhost:8088"

# Output CSV file path
CSV_FILE = "/app/data/prices.csv"

def fetch_prices():
    """Fetch current prices from the simulator"""
    try:
        response = requests.get(SIMULATOR_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None

def save_to_csv(data):
    """Save price data to CSV file"""
    #YOUR CODE HERE
    None
    

if __name__ == "__main__":
    print("Fetching prices...")
    data = fetch_prices()
    if data:
        save_to_csv(data)
        print("Done!")
    else:
        print("Failed to fetch prices") # Y que implica está linea?

