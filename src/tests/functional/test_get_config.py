from application.utils.util import get_config_base

def test_get_groups(app, client):
  response = client.get("/api/v1/groups")

  with app.app_context():
    groups = app.config["receiver_groups"]
    groups_list = [g.model_dump() for g in groups]

  assert response.status_code == 200
  assert response.json ["receiver_groups"] == groups_list

def test_get_config(app, client):
  response = client.get("/api/v1/config")

  with app.app_context():
    expected = get_config_base()

  assert response.status_code == 200
  assert response.get_json() == expected