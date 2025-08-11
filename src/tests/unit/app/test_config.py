import pytest
from app import create_app
from config import TestConfig, Config
from tests.fixtures.config_fixtures import PartialTestConfigFixture

expected_base_config = {
    "TESTING": True,
    "LOG_LEVEL_APP": "DEBUG",
    "LOG_LEVEL_HTTP": "DEBUG",
    "LOG_LEVEL_GUNICORN": "DEBUG",
    "TELIA_URL": "not-configured",
    "TELIA_USER": "not-configured",
    "TELIA_PW": "not-configured",
    "SMS_MAX_RECEIVERS": 20,
    "SMS_SENDER": "37250000000",
    "API_BASIC_AUTH_USER": "test1",
    "API_BASIC_AUTH_PW": "test1",
    "GROUPS_CONFIG_PATH": "tests/fixtures/receiver_groups_fixture.yaml"
}

expected_receiver_group = {
    "name": "test_group1",
    "description": "valid sms senders group",
    "receivers": [
        37256000001,
        37256000002,
        37256000003
    ]
}

def test_base_config_loaded(app):
    for key, expected_value in expected_base_config.items():
        assert app.config[key] == expected_value

def test_config_required_variable_missing():
    with pytest.raises(KeyError) as exc_info:
        app = create_app(PartialTestConfigFixture)

    assert "GROUPS_CONFIG_PATH" in str(exc_info.value) # KeyError

def test_receivers_config_loaded(app):
    assert "receiver_groups" in app.config
    assert isinstance(app.config.get("receiver_groups"), list)

    groups = app.config.get("receiver_groups")
    group = groups[0]
    assert group.name == expected_receiver_group["name"]
    assert group.description == expected_receiver_group["description"]
    assert group.receivers == expected_receiver_group["receivers"]

def test_receivers_config_loaded(app):
    assert "receiver_groups" in app.config
    assert isinstance(app.config.get("receiver_groups"), list)

    groups = app.config.get("receiver_groups")
    group = groups[0]
    assert group.name == expected_receiver_group["name"]
    assert group.description == expected_receiver_group["description"]
    assert group.receivers == expected_receiver_group["receivers"]