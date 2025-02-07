"""Counter API Implementation"""
from flask import Flask, jsonify, request
from . import status

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
  """Create a counter"""
  if counter_exists(name):
      return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
  COUNTERS[name] = 0
  return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

# Student 5: Increment a counter
@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
    """Increment the counter by 1."""
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
    COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

# Function #8: Prevent deleting non-existent counter
@app.route('/counters/<name>', methods=['DELETE'])
def deleting_nonexistent_counter(name):
   '''Prevent deleting non-existent counter'''
   if not counter_exists(name):
      return jsonify(name), status.HTTP_409_CONFLICT
   else:
      return jsonify(name), status.HTTP_200_OK

# Function #10: List counters
@app.route('/counters', methods=['GET'])
def list_counters():
    """List all counters"""
    # get just the counter names
    counterNames = list(COUNTERS.keys())
    return jsonify(counterNames), status.HTTP_200_OK 

# Function #11: Handle invalid HTTP methods [Ken Harvey]
@app.route('/counters/error/<id>', methods=['GET'])
def handle_invalid_http_methods(id):
  """Here, this route permits only GET,
     so long as no other permissions were set elsewhere for this route.
  """
  print('Setting GET as method for route: /counters/error/<id>')




