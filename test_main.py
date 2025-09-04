from fastapi.testclient import TestClient
from main import app
import pytest 

client = TestClient(app)

@pytest.mark.parametrize(
    "expected",
    [
        {'message': 'Hello FastAPI.'},
        {'message': 'Hello FastAPI.'},
        {'message': 'Hello FastAPI.'},
    ]
)

def test_root(expected):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == expected