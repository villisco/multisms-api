def test_get_health(client):
    response = client.get("/")
    assert response.json ["status"] == "up" 