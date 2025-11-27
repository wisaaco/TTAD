#!/usr/bin/env python3
"""
Simple Flask status server to keep the student-container running.
FOR MY SIMPLICITY !!!
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/status', methods=['GET'])
def status():
    """Return container status"""
    return jsonify({"status": "live"})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting status server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)

