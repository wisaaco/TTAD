#!/usr/bin/env python3
"""
Example script to fetch prices from the simulator and save to CSV
This is a starting point - students should modify and improve this script
"""

import requests
import os
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
    # data = {"products":{"Seitan":{"coin":"dollar","price":2.22,"quantity":"200g"},"Tempe":{"coin":"euro","price":3.38,"quantity":"200g"},"Tofu":{"coin":"euro","price":10.04,"quantity":"400g"}},"time":10,"timestamp":"2025-12-05T07:27:28.366830"}
    
    # Si el fichero no existe podemos crear el header del CSV
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w") as f:
            f.write("product_name,product_price,product_quantity,product_coin,product_time,product_timestamp\n")

    # Añadimos muestras en el fichero usando simplemente una linea por cada muestra, y lo tratamos como un fichero de texto plano. Este tiene tres modos de apertura: "r" - solo lectura, "w" - write sobreescribiendo, "a" - write appending.
    with open(CSV_FILE, "a") as f:
        for keys_products in data["products"]:
            print(keys_products)
            product_name = keys_products
            product_price = data["products"][product_name]["price"]
            product_quantity = data["products"][product_name]["quantity"]
            product_coin = data["products"][product_name]["coin"]
            product_time = data["time"]
            product_timestamp = data["timestamp"]
            f.write(f"{product_name},{product_price},{product_quantity},{product_coin},{product_time},{product_timestamp}\n")
    

if __name__ == "__main__":
    print("Fetching prices...")
    data = fetch_prices()
    if data:
        save_to_csv(data)
        print("Done!")
    else:
        print("Failed to fetch prices") # Y que implica está linea?

