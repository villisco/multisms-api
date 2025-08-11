def test_internal_server_error_returns_json(client, app):
    @app.route("/raise500")
    def raise_500():
        raise Exception("Simulated failure")

    response = client.get("/raise500")
    assert response.status_code == 500

    json_body = response.get_json()
    assert "id" in json_body
    assert json_body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert json_body["error"]["message"] == "An unexpected error occurred."

def test_not_found_error_returns_json(client):
    response = client.get("/nonexistent-endpoint")

    assert response.status_code == 404

    json_body = response.get_json()
    assert "id" in json_body
    assert json_body["error"]["code"] == "HTTP_404"
    assert "not found" in json_body["error"]["message"].lower()