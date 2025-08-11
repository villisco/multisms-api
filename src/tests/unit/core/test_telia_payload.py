import pytest
from dataclasses import dataclass
from application.core.telia_payload import TeliaPayload
from application.utils.exceptions import ApiException, ApiError

# Dummy ReceiverGroup class
@dataclass
class ReceiverGroup:
    name: str

@pytest.mark.parametrize(
    "configured_group_names, request_groups, expected",
    [
        (["group1", "group2"], ["group1"], True),
        (["group1", "group2"], ["group1", "group2"], True),
        (["group1", "group2"], ["group3"], False),
        (["group1"], ["group1", "group2"], False),
        (["group1", "group2"], [], False),  # Empty input not allowed
        ([], ["group1"], False),
    ],
    ids=[
        "group-match",
        "groups-match",
        "nonexistent-group",
        "partial-match",
        "empty-input-valid",
        "no-config-groups"
    ]
)
def test_verify_request_groups_exist(app, configured_group_names, request_groups, expected):
    with app.app_context():
        app.config["receiver_groups"] = [ReceiverGroup(name=name) for name in configured_group_names]
        payload = TeliaPayload()
        result = payload._verify_groups_exist(request_groups)
        assert result == expected


def test_prepare_payload_raises_on_invalid_group(monkeypatch, app):
    payload = TeliaPayload()

    monkeypatch.setattr(payload, "_verify_groups_exist", lambda groups: False)

    with app.app_context():
        with pytest.raises(ApiException) as exc_info:
            payload.prepare_payload(["invalid_group"], "hello")

    assert exc_info.value.status_code == 400
    assert exc_info.value.code == ApiError.UNKNOWN_RECEIVER_GROUP["code"]

def test_validate_sms_text_length_valid():
    payload = TeliaPayload()
    short_text = "a" * 1530  # Exactly at the limit

    assert payload._validate_sms_text_length(short_text) is True


def test_validate_sms_text_length_too_long():
    payload = TeliaPayload()
    long_text = "a" * 1531  # Just over the limit

    with pytest.raises(ValueError) as exc_info:
        payload._validate_sms_text_length(long_text)

    assert "SMS message exceeded allowed characters" in str(exc_info.value)