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

    # Test #2: Prevent duplicate counters
    # [Please list your name as well]
    def test_prevent_duplicate_counters(self, client):
        """It should prevent creating a duplicate counter"""
        # create a counter
        client.post('/counters/foo')
        # attempt to create the same counter
        result = client.post('/counters/foo')
        # check if we were successful
        assert result.status_code == status.HTTP_409_CONFLICT

    # Test #3: Retrieve an existing counter.
    def test_retrieve_existing_counter(self, client):
        """It should retrieve an existing counter"""
        # create a test counter
        client.post('/counters/retrieveCounterTest')
        # retrieve counter using GET method
        response = client.get('/counters/retrieveCounterTest')
        # verify succesful request
        assert response.status_code == status.HTTP_200_OK

    # Test #3: Return 404 for non-existent counter
    # Tanner Donovan
            def test_return_404_for_non_existent_counter(self, client):
        """Test that a 404 is returned for a non-existent counter"""
        result = client.get('/counters/nonexistent')
        assert result.status_code == status.HTTP_404_NOT_FOUND
        
=======
    # Test #5: Increment existing counter.
    def test_increment_counter(self, client):
            """It should increment an existing counter using PUT /counters/<name>."""
            # Counter named 'incrementTest'
            create_response = client.post('/counters/incrementTest')
            assert create_response.status_code == status.HTTP_201_CREATED
            # Increment the counter using PUT
            put_response = client.put('/counters/incrementTest')
            assert put_response.status_code == status.HTTP_200_OK
            # Verify that the counter's value is now incremented by 1
            data = put_response.get_json()
            assert "incrementTest" in data
            assert data["incrementTest"] == 1

    # Test #7: Delete a counter
    def test_delete_counter(self, client):
        """It should delete a counter"""
        # create a counter to be deleted
        client.post('/counters/boo')
        # delete the counter
        result = client.delete('/counters/boo')
        # check if we were successful
        assert result.status_code == status.HTTP_200_OK

    # Test #8: Prevent deleting non-existent counter
    def test_deleting_nonexistent_counter(self, client):
        '''It should prevent deleting a non-existent counter'''
        # Attempting to delete counter that doesn't exist
        result = client.delete('/counters/testcounter')
        # Check if a conflict status code was returned
        assert result.status_code == status.HTTP_409_CONFLICT

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


    # Test #11, Handle invalid HTTP methods [Ken Harvey]
    def test_handle_invalid_http_methods(self, client):
        """Fails to catch un-allowed HTTP method unless a route is created
           which disallows the method.
           Once the route /counters/error/<id> is created (in counter.py) with
           methods=['GET'], the following post will indeed return 405"""
        result = client.post('/counters/error/id')  # line#1 POST is not allowed on this route
        # result = client.get('/counters/error/id') # line#2 this is ok
        assert result.status_code != status.HTTP_404_NOT_FOUND             # route exists
        assert result.status_code == status.HTTP_405_METHOD_NOT_ALLOWED    # route method is invalid
 
