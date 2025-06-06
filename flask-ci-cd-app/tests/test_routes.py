import sys
import os

# Manually add the project root (parent of 'tests') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import create_app
import pytest

# Define a reusable pytest fixture that sets up a test client
@pytest.fixture
def client():
    app = create_app()
    return app.test_client()



def test_home(client):
    response = client.get('/')
    assert response.status_code == 200




def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == "ok"