import logging
import pytest
from flask import Flask
import requests

from application.services.telia_api import TeliaMultiSmsAPI
from application.utils.exceptions import ApiException, ApiError


class FakeResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data if json_data is not None else {}

    def json(self):
        return self._json

    def raise_for_status(self):
        # Mimic requests' behavior: raise on 4xx/5xx
        if 400 <= self.status_code:
            raise requests.HTTPError(f"{self.status_code} error", response=self)


@pytest.fixture
def flask_app_ctx():
    app = Flask(__name__)
    app.testing = True
    with app.app_context():
        yield app


@pytest.fixture
def service():
    return TeliaMultiSmsAPI(base_url="https://api.example.com", user="u", password="p")

def test_post_request_success_returns_response(flask_app_ctx, service, monkeypatch):
    payload = {"k": "v"}

    def _post(url, auth=None, headers=None, json=None, verify=None):
        # basic sanity checks (optional)
        assert url.endswith("/sms")
        assert auth == ("u", "p")
        assert headers["Accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"
        assert json == payload
        assert verify is True
        return FakeResponse(200, {"ok": True})

    monkeypatch.setattr(requests, "post", _post)

    resp = service._post_request(payload)
    assert isinstance(resp, FakeResponse)
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_post_request_http_error_maps_to_service_error(flask_app_ctx, service, monkeypatch, caplog):
    payload = {"k": "v"}

    def _post(*args, **kwargs):
        return FakeResponse(400, {"error": "bad request"})

    monkeypatch.setattr(requests, "post", _post)
    caplog.set_level(logging.ERROR)

    with pytest.raises(ApiException) as ei:
        service._post_request(payload)

    err = ei.value
    # ApiException stores only the code/message from the dict. Assert on `code`.
    assert err.code == ApiError.TELIA_SERVICE_ERROR["code"]
    assert err.status_code == 502
    # log line should mention "unexpected error"
    assert any("Telia REST API unexpected error" in rec.message for rec in caplog.records)


def test_post_request_connection_error_maps_to_connection_failed(flask_app_ctx, service, monkeypatch, caplog):
    payload = {"k": "v"}

    def _post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("boom")

    monkeypatch.setattr(requests, "post", _post)
    caplog.set_level(logging.ERROR)

    with pytest.raises(ApiException) as ei:
        service._post_request(payload)

    err = ei.value
    assert err.code == ApiError.TELIA_CONNECTION_FAILED["code"]
    assert err.status_code == 502
    assert any("Failed to connect to Telia REST API" in rec.message for rec in caplog.records)


def test_post_request_timeout_maps_to_timeout(flask_app_ctx, service, monkeypatch, caplog):
    payload = {"k": "v"}

    def _post(*args, **kwargs):
        raise requests.exceptions.Timeout("slow")

    monkeypatch.setattr(requests, "post", _post)
    caplog.set_level(logging.ERROR)

    with pytest.raises(ApiException) as ei:
        service._post_request(payload)

    err = ei.value
    assert err.code == ApiError.TELIA_TIMEOUT["code"]
    assert err.status_code == 504
    assert any("request timed out" in rec.message for rec in caplog.records)


def test_post_request_unexpected_exception_maps_to_service_error(flask_app_ctx, service, monkeypatch, caplog):
    payload = {"k": "v"}

    def _post(*args, **kwargs):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(requests, "post", _post)
    caplog.set_level(logging.ERROR)

    with pytest.raises(ApiException) as ei:
        service._post_request(payload)

    err = ei.value
    assert err.code == ApiError.TELIA_SERVICE_ERROR["code"]
    assert err.status_code == 502
    assert any("unexpected error" in rec.message.lower() for rec in caplog.records)