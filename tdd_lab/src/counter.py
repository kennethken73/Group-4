"""
Counter API Implementation
"""

from flask import Flask, jsonify, request
from src import status

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
    """Check if a counter exists"""
    return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
    """Increment an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": "Counter does not exist"}), 404
    # Increment the counter value
    COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), 200