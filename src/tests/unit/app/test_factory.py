import pytest
from config import TestConfig
from app import create_app

def test_app_created_with_test_config():
    assert create_app(TestConfig).testing

def test_create_app_fails_without_receivers_config():
    class BadConfig:
        TESTING = True
        GROUPS_CONFIG_PATH = ""

    with pytest.raises(RuntimeError, match="GROUPS_CONFIG_PATH"):
        app = create_app(BadConfig)