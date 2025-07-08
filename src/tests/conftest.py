import os
import sys
import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient

# ensure src/ is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def dummyjson_mock():
    """
    Automatically mock calls to DummyJSON endpoints for todos and users.
    """
    with respx.mock as mock:
        mock.get("https://dummyjson.com/todos").respond(
            200,
            json={
                "todos": [
                    {"id": 1, "todo": "Buy milk",       "completed": False, "userId": 42},
                    {"id": 2, "todo": "Write tests",    "completed": True,  "userId": 42},
                    {"id": 3, "todo": "Deploy service", "completed": False, "userId": 99},
                ]
            }
        )
        mock.get("https://dummyjson.com/users").respond(
            200,
            json={
                "users": [
                    {"id": 42, "username": "alice"},
                    {"id": 99, "username": "bob"},
                ]
            }
        )
        yield