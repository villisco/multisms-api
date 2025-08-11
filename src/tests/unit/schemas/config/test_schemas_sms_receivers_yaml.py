import pytest
from pydantic import ValidationError
from application.schemas.config.sms_receivers_yaml import ReceiverGroup

def test_valid_receivers():
    group = ReceiverGroup(
        name="test",
        sender="OK",
        receivers=[37256111111, 56111112],
    )
    assert len(group.receivers) == 2

def test_receiver_does_not_start_with_5_or_372():
    with pytest.raises(ValidationError) as exc_info:
        ReceiverGroup(
            name="test",
            sender="OK",
            receivers=[412345678],
        )
    assert "must start with 5 or 372" in str(exc_info.value)

def test_receiver_too_long():
    with pytest.raises(ValidationError) as exc_info:
        ReceiverGroup(
            name="test",
            sender="OK",
            receivers=[512345678901],  # 12 digits
        )
    assert "must not be longer than 11 digits" in str(exc_info.value)

def test_receiver_list_not_list():
    with pytest.raises(ValidationError) as exc_info:
        ReceiverGroup(
            name="test",
            sender="OK",
            receivers="37256111111",  # Not a list
        )
    assert "must be a list of integers" in str(exc_info.value)