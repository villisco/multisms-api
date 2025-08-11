def test_unknown_endpoint(client):
    response = client.get("/not-existing")
    assert response.status_code == 404