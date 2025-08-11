import logging
import pytest
from flask import Flask

from application.utils.util import response_to_pydantic_model  # <- your module path
from application.schemas.services.telia_responses import TeliaSuccessResponse
from application.utils.exceptions import ApiException, ApiError


class _FakeResponseInvalidJSON:
    status_code = 200
    text = "not a json payload"

    def json(self):
        # Simulate requests.Response.json() failing to parse
        raise ValueError("No JSON object could be decoded")


class _FakeResponseSchemaMismatch:
    status_code = 200
    text = '{"foo": "bar"}'  # valid JSON text but wrong shape

    def json(self):
        # Valid JSON but does not conform to TeliaSuccessResponse
        return {"foo": "bar"}


@pytest.fixture
def flask_app_context():
    app = Flask(__name__)
    app.testing = True
    with app.app_context():
        yield app


def test_response_to_pydantic_model_invalid_json_raises_api_exception(flask_app_context, caplog):
    fake_resp = _FakeResponseInvalidJSON()
    caplog.set_level(logging.ERROR)

    with pytest.raises(ApiException) as ei:
        response_to_pydantic_model(fake_resp, TeliaSuccessResponse)

    err = ei.value
    assert err.code == ApiError.TELIA_INVALID_RESPONSE_FORMAT["code"]
    assert err.status_code == 502
    assert err.details == {"Response text": fake_resp.text[:200]}

    assert any(
        "Failed to parse Telia API response into" in rec.message
        and "TeliaSuccessResponse" in rec.message
        for rec in caplog.records
    )


def test_response_to_pydantic_model_schema_mismatch_raises_api_exception(flask_app_context, caplog):
    fake_resp = _FakeResponseSchemaMismatch()

    caplog.set_level(logging.ERROR)

    with pytest.raises(ApiException) as exc:
        response_to_pydantic_model(fake_resp, TeliaSuccessResponse)

    err = exc.value
    assert err.code == ApiError.TELIA_INVALID_RESPONSE_FORMAT["code"]
    assert err.status_code == 502
    assert err.details == {"Response text": fake_resp.text[:200]}

    # Make sure we logged the ValidationError path too
    assert any(
        "Failed to parse Telia API response into" in rec.message
        and "TeliaSuccessResponse" in rec.message
        for rec in caplog.records
    )