#!/usr/bin/env python3
"""
Price Simulator - Generates product prices with independent trends
Updates every 10 seconds with price variations and occasional quantity changes
"""

import time
import random
import json
import threading
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Initial product data
products = {
    "Tofu": {
        "price": 10.0,
        "quantity": "200g",
        "coin": "euro",
        "trend": random.choice([-1, 1]),  # -1 for decreasing, 1 for increasing
        "trend_strength": random.uniform(0.01, 0.05),  # Price change per update
        "base_price": 10.0
    },
    "Seitan": {
        "price": 2.0,
        "quantity": "100g",
        "coin": "dollar",
        "trend": random.choice([-1, 1]),
        "trend_strength": random.uniform(0.02, 0.08),
        "base_price": 2.0
    },
    "Tempe": {
        "price": 3.99,
        "quantity": "200g",
        "coin": "euro",
        "trend": random.choice([-1, 1]),
        "trend_strength": random.uniform(0.015, 0.06),
        "base_price": 3.99
    }
}

# Quantity options for each product
quantity_options = {
    "Tofu": ["200g", "300g", "400g", "500g"],
    "Seitan": ["100g", "150g", "200g", "250g"],
    "Tempe": ["200g", "250g", "300g", "350g"]
}

update_counter = 0

def update_prices():
    """Update prices with independent trends and occasional quantity changes"""
    global update_counter
    update_counter += 1
    
    for product_name, product_data in products.items():
        # Update price based on trend
        trend_direction = product_data["trend"]
        trend_strength = product_data["trend_strength"]
        
        # Add some randomness to the trend
        price_change = trend_direction * trend_strength * random.uniform(0.5, 1.5)
        new_price = product_data["price"] + price_change
        
        # Ensure price doesn't go below 0.1
        new_price = max(0.1, new_price)
        
        # Occasionally reverse the trend (10% chance)
        if random.random() < 0.1:
            product_data["trend"] *= -1
        
        # Occasionally change trend strength (5% chance)
        if random.random() < 0.05:
            product_data["trend_strength"] = random.uniform(0.01, 0.08)
        
        product_data["price"] = round(new_price, 2)
        
        # Occasionally change quantity (15% chance every update)
        if random.random() < 0.15:
            current_qty = product_data["quantity"]
            available_quantities = [q for q in quantity_options[product_name] if q != current_qty]
            if available_quantities:
                product_data["quantity"] = random.choice(available_quantities)

def price_update_loop():
    """Background thread that updates prices every 10 seconds"""
    while True:
        time.sleep(10)  # Update every 10 seconds
        update_prices()
        print(f"Prices updated (counter: {update_counter})")

@app.route('/', methods=['GET'])
def get_prices():
    """Return current product prices as JSON"""
    # Prices are updated automatically in background, just return current state
    
    # Format response according to the example in README
    response = {
        "time": update_counter,
        "timestamp": datetime.now().isoformat(),
        "products": {
            name: {
                "price": data["price"],
                "quantity": data["quantity"],
                "coin": data["coin"]
            }
            for name, data in products.items()
        }
    }
    
    return jsonify(response)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting Price Simulator on port 8088...")
    print("Products available: Tofu, Seitan, Tempe")
    print("Prices update every 10 seconds with independent trends")
    
    # Start background thread for price updates
    update_thread = threading.Thread(target=price_update_loop, daemon=True)
    update_thread.start()
    
    # Initial price update
    update_prices()
    
    # Run Flask app with threading enabled
    app.run(host='0.0.0.0', port=8088, debug=False, threaded=True, use_reloader=False)

