"""
Test Cases for Counter Web Service
Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest
from src import app
from src import status
# from . import counter #for test #11

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    # Test #10, listing all counters
    def test_list_counters(self, client):
        """It should list all counters"""
        # creating test counters
        client.post('/counters/testcounter1')
        client.post('/counters/testcounter2')
        client.post('/counters/testcounter3')

        # use .get to get counters and HTTP status code
        getcounters = client.get('/counters')
        # check if we were successful
        assert getcounters.status_code == status.HTTP_200_OK
        # get the actual list to verify
        counterlist = getcounters.get_json()
        # check if test counters are in the list
        assert "testcounter1" in counterlist
        assert "testcounter2" in counterlist
        assert "testcounter3" in counterlist


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
    ############################################################################
    # ### idea1
    # def test_warn_if_http_method_is_unsupported(self, client):
    #     """If warn_if_http_method_is_unsupported() works right,
    #     then a get request to a route without GET method authorization
    #     """
    #     msg = client.post('/counters/e405')  #creates '/counter/e405'
    #     # d_result = client.delete('/counters/e405')  #should fail as 'delete' isn't authorized?

    #     # get_msg = client.get('/counters/e405')
    #     # Above does not fail, even though get_msg.status_code == 405
    #     # assert get_msg.status_code == status.HTTP_200_OK
    #     # msg_status_code = get_msg.status_code
    #     # assert get_msg.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #     # assert warn_if_http_method_is_unsupported(msg_status_code) == "warn"
        
    #     response = client.post('/counters/test_405')
    #     unsupported_delete_response = client.delete('/counters/test_405')
    #     assert unsupported_delete_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # ###

    ### idea2
    # def test_method_is_supported(route, method):
    #     assert method_is_supported(route, client, method) == True

#NOTE this_test(self, client) here in test_counter
#  while test(route, method) ..
