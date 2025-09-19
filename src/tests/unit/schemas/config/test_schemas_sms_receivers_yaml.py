import pytest
from pydantic import ValidationError
from application.schemas.config.sms_receivers_yaml import ReceiverGroup, Receiver

def test_valid_receivers():
    group = ReceiverGroup(
        name="test",
        description="OK",
        receivers=[
            {"number": "37256111111", "name": "User A"},
            {"number": "56111112",    "name": "User B"},
        ],
    )
    assert len(group.receivers) == 2
    assert [r.number for r in group.receivers] == ["37256111111", "56111112"]
    assert [r.name for r in group.receivers] == ["User A", "User B"]

def test_receiver_does_not_start_with_5_or_372():
    with pytest.raises(ValidationError) as exc_info:
        ReceiverGroup(
            name="test",
            description="OK",
            receivers=[{"number": "412345678", "name": "Not Local Mobile Number"}],
        )
    assert "must start with '5' or '372'" in str(exc_info.value)

def test_receiver_too_long():
    with pytest.raises(ValidationError) as exc_info:
        ReceiverGroup(
            name="test",
            description="OK",
            receivers=[
                {"number": "372560000011111111111111111111111", "name": "Number Toolong"},
            ],
        )
    # Message from Receiver.validate_number
    assert "Receiver number must not be longer than 11 digits" in str(exc_info.value)

def test_receivers_schema_objects_ok():
    g = ReceiverGroup(
        name="test_group",
        receivers=[
            {"number": "37256000001", "name": "User 1"},
            {"number": "37256000002", "name": "User 2"},
        ],
    )
    assert len(g.receivers) == 2
    assert g.receivers[0].number == "37256000001"
    assert g.receivers[0].name == "User 1"

def test_receiver_number_must_contain_only_digits_simple():
    with pytest.raises(ValidationError) as exc_info:
        Receiver(number="3725-600001", name="Test User")  # hyphen makes it non-digit
    assert "Receiver number must contain only digits" in str(exc_info.value)