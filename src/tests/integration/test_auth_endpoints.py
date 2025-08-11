from application.utils.exceptions import ApiError

def test_health_endpoint_no_auth(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json ["status"] == "up"

def test_sms_endpoint_no_auth(client):
    response = client.post("/api/v1/sms", json={"message": "Test"})
    assert response.status_code == 401
    assert ApiError.AUTH_BASIC_REQUIRED["message"] in response.json["error"]["message"]
    assert ApiError.AUTH_BASIC_REQUIRED["code"] in response.json["error"]["code"]

def test_alertmanager_endpoint_no_auth(client):
    response = client.post("/api/v1/webhooks/alertmanager", json={"message": "Test"})
    assert response.status_code == 401
    assert ApiError.AUTH_BASIC_REQUIRED["message"] in response.json["error"]["message"]
    assert ApiError.AUTH_BASIC_REQUIRED["code"] in response.json["error"]["code"]

def test_health_endpoint_with_auth(client, default_auth_header):
    response = client.get("/", headers=default_auth_header)
    assert response.status_code == 200
    assert response.json ["status"] == "up"

def test_sms_endpoint_with_auth(client, default_auth_header):
    response = client.post("/api/v1/sms", json={"message": "Test"}, headers=default_auth_header)
    assert not response.status_code == 401

def test_alertmanager_endpoint_with_auth(client, default_auth_header):
    response = client.post("/api/v1/webhooks/alertmanager", json={"message": "Test"}, headers=default_auth_header)
    assert not response.status_code == 401