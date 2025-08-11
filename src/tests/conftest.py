"""
NB! Global fixtures are defined here!

Fixtures defined in a conftest.py can be used by any test in that package 
without needing to import them (pytest will automatically discover them).

https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""
import pytest
import base64
import json
from requests.models import Response
from config import TestConfig
from app import create_app

def basic_auth_header(username: str, password: str) -> dict:
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

@pytest.fixture()
def dict_to_response():
    def _convert(response_data: dict, status_code: int = 200) -> Response:
        """
        Returns a function that converts a dict to a Response object.
        """
        response = Response()
        response.status_code = status_code
        response._content = json.dumps(response_data).encode('utf-8')  # Set raw content as bytes
        response.headers['Content-Type'] = 'application/json'
        return response
    
    return _convert

@pytest.fixture()
def load_mock_json():
    def _loader(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
    return _loader

@pytest.fixture()
def app():
    """
    globally usable app for tests (factory)
    """
    app = create_app(TestConfig)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def default_auth_header(app):
    username = app.config["API_BASIC_AUTH_USER"]
    password = app.config["API_BASIC_AUTH_PW"]
    return basic_auth_header(username, password)