from application.utils.util import loaded_config

def test_get_config(app, client):
  response = client.get("/api/v1/config")

  with app.app_context():
    config = loaded_config()
    expected_env_vars = config["env_vars"]
    expected_groups = config["receiver_groups"]

  assert response.status_code == 200
  assert response.json ["env_vars"] == expected_env_vars
  assert response.json ["receiver_groups"] == expected_groups