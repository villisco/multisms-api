import pytest
from application.schemas.services.telia_payload import SmsMessage, SmsMessages

def test_sms_message_valid():
    msg = SmsMessage(**{
        "flash": False,
        "from": "SUPPORTED_SENDER",
        "message": "Hello!",
        "requestReport": True,
        "to": "372561111111"
    })
    assert msg.message == "Hello!"

def test_sms_messages_len():
    # Empty list
    empty_messages = SmsMessages(messages=[])
    assert len(empty_messages) == 0

    # Single message
    one_message = SmsMessages(messages=[
        SmsMessage(
            flash=False,
            from_="SENDER1",
            message="Hello",
            requestReport=True,
            to="372561111111"
        )
    ])
    assert len(one_message) == 1

    # Multiple messages
    multiple_messages = SmsMessages(messages=[
        SmsMessage(
            flash=True,
            from_="SENDER1",
            message="Msg1",
            requestReport=False,
            to="372561111111"
        ),
        SmsMessage(
            flash=False,
            from_="SENDER2",
            message="Msg2",
            requestReport=True,
            to="372562222222"
        ),
    ])
    assert len(multiple_messages) == 2