def test_get_index(client):
    response = client.get("/")
    body = response.data

    assert response.status_code == 200
    assert response.mimetype == "application/xhtml+xml"
    assert response.mimetype_params.get("charset", "").lower() in ("utf-8", "utf8")

    assert body.startswith(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    assert b"<h1>Current configuration</h1>" in body
    assert b"<h2>App Configuration</h2>" in body
    assert b"<h2>Receiver Groups</h2>" in body