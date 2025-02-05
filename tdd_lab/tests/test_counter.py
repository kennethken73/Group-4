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

    def test_increment_counter(self, client):
        """It should increment an existing counter"""
        
        
        create_response = client.post('/counters/test_counter')
        assert create_response.status_code == 201 

        increment_response = client.put('/counters/test_counter')
        assert increment_response.status_code == 200 

        data = increment_response.get_json()
        assert data["test_counter"] == 1