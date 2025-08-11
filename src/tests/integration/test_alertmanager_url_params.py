def test_alertmanager_url_params_missing(client, default_auth_header):
    response = client.post("/api/v1/webhooks/alertmanager", headers=default_auth_header)
    assert response.status_code == 422 # validation error

def test_alertmanager_url_params_unknown(client, default_auth_header):
    response = client.post("/api/v1/webhooks/alertmanager?unknown_param=test1", headers=default_auth_header)
    assert response.status_code == 422 # validation error