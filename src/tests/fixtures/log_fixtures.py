import pytest
import logging

@pytest.fixture
def werkzeug_log_before_date_filter():
    return logging.LogRecord(
        name="werkzeug",
        level=logging.INFO,
        pathname="test",
        lineno=1,
        msg='192.168.0.102 - - [30/Jun/2024 01:14:03] "GET / HTTP/1.1" 200 123',
        args=(),
        exc_info=None
    )

@pytest.fixture
def werkzeug_log_after_date_filter():
    return logging.LogRecord(
        name="werkzeug",
        level=logging.INFO,
        pathname="test",
        lineno=1,
        msg='192.168.0.102 - "GET / HTTP/1.1" 200 123',
        args=(),
        exc_info=None
    )

@pytest.fixture
def werkzeug_log_filtered_head_req():
    return logging.LogRecord(
        name="werkzeug",
        level=logging.INFO,
        pathname="test",
        lineno=1,
        msg='192.168.0.102 - "HEAD / HTTP/1.0" 200 -',
        args=(),
        exc_info=None
    )