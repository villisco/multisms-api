from flask import request
from flask import current_app as app
from application.utils.exceptions import ApiException, ApiError
from config import AuthSecurity

def basic_auth_check():
    """
    Alertmanager supports Basic Auth:

    receivers:
      - name: "webhook-with-token"
        webhook_configs:
          - url: "https://my-receiver.local/webhook"
            send_resolved: true
            http_config:
              bearer_token: /etc/alertmanager/webhook_token.txt
    """
    if request.path in AuthSecurity.secured_endpoints:
      auth = request.authorization

      if auth:
          is_passed = (auth.username == app.config["API_BASIC_AUTH_USER"] and auth.password == app.config["API_BASIC_AUTH_PW"])
      else:
          is_passed = False

      if not is_passed: 
        raise ApiException(ApiError.AUTH_BASIC_REQUIRED, status_code=401)
