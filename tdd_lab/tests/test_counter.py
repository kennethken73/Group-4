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
            