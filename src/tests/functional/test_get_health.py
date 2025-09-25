def test_get_health(client):
    response = client.get("/api/v1/health")
    assert response.json ["status"] == "up" 