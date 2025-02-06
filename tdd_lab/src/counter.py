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

############################################################################
# Test #11.:  Handle invalid HTTP methods.
#             Targeting Unsupported HTTP Methods
#
# Name:       Ken Harvey
# Test-name:  test_bad_http_api_call_is_handled()
# TDD cure:   src/counter.py:method_not_allowed(err)
#
# Citations:
# 1. google query: "what are the flask api http methods"
#    Found:        https://www.geeksforgeeks.org/flask-http-method/
#    AI suggests:  AI gave a list and brief description of supported methods
# 2. google query: "how to handle an unsupported http method in flask"
#    AI suggests:  AI suggestion appended to my lab report.
#                  Using this as a starting point,
#                  as I've zero previous python experience, much less flask.
# 3. google query: "flask get list of allowed http methods"
#    AI suggests:  allowed_methods = request.url_rule.methods
#
# Learned:   1. Apparently a flask 'route' is a location on dir tree.
#            2. Routes are assigned methods
#            3. @ syntax is for 'Python Decorators'
#
#    @app.errorhandler(405)
#    def method_not_allowed(e):
#         return jsonify({'error': 'Method Not Allowed'}), 405
############################################################################
# @app.route('/counters')
# def warn_if_http_method_is_unsupported(msg_status_code):
#     look = request.args.get("")
#     return "warn"

# @app.route('<route>')
# def method_is_supported(route, client, method):
#     if request.method == 'POST':
#         result = client.post(route)
#     return False

